from utils.constants import ATTR_MEANING, GAMES_ATTRIB, PLAYERS_ATTRIB, TEAMS, TEAMS_ATTRIB
from utils.enrichment import games_new_attr, games_id_and_check
from utils.logger import logger
from typing import List
import pandas as pd
import sqlite3
import glob
import numpy as np

"""
From the data coming from rotowire, one csv per "week" per league per season, where a row corresponds to how a player
did play during on game (with all the attributes).

Steps : 
- Download proper data from rotowire.com, and name it properly '{league}_{season}_{file}.csv'.
- concat_csv : Concat all the files into one and add attributes to make sql request easier.
- Add the exported file to bigquery bucket.
- compute_games : From all the players of specific league / seasons, deduce games.
- enrich_players : From all the players and the export files of players2games, get as much infos per players.
"""


def get_files(files_dir: List[str]):
    files = {}
    for file in files_dir:
        file = file[:-4]
        file_nbr = int(str(file).split('_')[-1])
        files[file_nbr] = file + '.csv'

    return files


def players_2sql(leagues: List[str], seasons: List[str], db: str = '../rotowire/database/PlayersInfo.db'):
    """
    From all the csv of seasons and leagues, will concat into one sql database.
    Moreover, the attributes names and the different teams are made more meaningful. And attributes league,
    season, week, file are add to make sql queries easier.
    :param leagues: List[str]. All the desired league.
    :param seasons: List. All the desired season.
    :param db: str. Path to the database containing the games.
    :return: Export the sql database PlayersInfo.db in rotowire/database.
    """
    conn = sqlite3.connect(db)
    logger.info(f'Adding players info to database for leagues : {leagues} and seasons : {seasons}')

    for league in leagues:
        for season in seasons:
            files_dir = glob.glob(f'../rotowire/{league}/players/{season}/*.csv')
            files = get_files(files_dir)

            season_league = []
            for i in range(1, len(files) + 1):
                csv = pd.read_csv(files[i]).rename(columns=ATTR_MEANING)
                try:
                    csv['team'] = csv.team.apply(lambda x: TEAMS[league][x])
                except KeyError:
                    logger.info(f"The following team's name must be add to TEAM[{league}] : "
                                f"{set(csv.team.unique()) - set(TEAMS[league].keys())} (from file {i}).")
                    breakpoint()

                csv['opponent'] = csv.opponent.apply(lambda x: TEAMS[league][x])
                csv['league'] = [league] * len(csv)
                csv['season'] = [season] * len(csv)
                csv['file'] = [i] * len(csv)

                season_league.append(csv)

            df_season_league = pd.concat(season_league, ignore_index=True, sort=False)
            df_season_league.to_sql(f'{league}_{season}', con=conn, if_exists='replace', index=False)


def _get_game(df_team, week, i):
    df_opp = week.query(f"team == '{df_team.opponent.values[0]}' and opponent == '{df_team.team.values[0]}'")

    if df_team.home_away.values[0] == 'H':
        df_home, df_away = df_team, df_opp
    elif df_team.home_away.values[0] == 'A':
        df_home, df_away = df_opp, df_team
    else:
        raise ValueError("A team cannot play neither at home and away")

    id_nb = pd.DataFrame({'id_home': [f'{i}_{df_home.team.values[0]}'],
                          'id_away': [f'{i}_{df_away.team.values[0]}']})

    game_info = pd.DataFrame({'home': df_home.team.unique(),
                              'away': df_away.team.unique(),
                              'league': df_away.league.unique(),
                              'season': df_away.season.unique(),
                              'file': df_away.file.unique(),
                              'h_formation': [df_home.formation.unique()[0]],
                              'a_formation': [df_away.formation.unique()[0]],
                              'week': [i],
                              'h_goals_conceded': [df_home.goals_conceded.unique()[0]],
                              'a_goals_conceded': [df_away.goals_conceded.unique()[0]]})

    df_home.drop(columns=['player_name', 'team', 'opponent', 'home_away', 'formation', 'position',
                          'games_played', 'minutes', 'starts', 'sub_on', 'sub_off',
                          'league', 'season', 'file', 'goals_conceded'], inplace=True)
    df_away.drop(columns=['player_name', 'team', 'opponent', 'home_away', 'formation', 'position',
                          'games_played', 'minutes', 'starts', 'sub_on', 'sub_off',
                          'league', 'season', 'file', 'goals_conceded'], inplace=True)

    df_home.rename(columns={x: 'h_' + x for x in df_home.keys()}, inplace=True)
    df_away.rename(columns={x: 'a_' + x for x in df_away.keys()}, inplace=True)

    game = pd.concat([id_nb,
                      game_info,
                      df_home.sum().to_frame().transpose(),
                      df_away.sum().to_frame().transpose()],
                     axis=1, sort=False)

    return game


def compute_games(league: str, season: str, db: str = '../rotowire/database/PlayersInfo.db') -> pd.DataFrame:
    """
    This methods goes from a directory to a csv files that will be export.
    The directory should contains different stats per players among one season and as much csv as week played.
    The csv' name should finish i.csv where i corresponds to week.
    Moreover, since the attributes from rotowire are not explicit enough, we will use the dictionary ATTR_MEANING
    to make them more readable.
    The export csv represent all the df_games that has been happening during one season. Per df_games, different id are
    added, every attributes starting with h_ (a_) represent the home (away) team.

    :param league: str. League names ('ligue1', 'bundesliga', 'premiere_league' ...).
    :param season: str. Wanted season ('1718', '1920' ...).
    :param db: str. Path to the database containing the games.
    :return: pd.Dataframe. Dataframe with all the df_games for one season.
    """
    from utils.fix_postponed import fix_postponed
    from utils.enrichment import score_and_points
    logger.info(f'Computing games for league : {league} and season : {season}')

    conn = sqlite3.connect(db)
    data = pd.read_sql_query(f'SELECT * FROM {league}_{season}', con=conn)

    def _to_name(week):
        i = week.file.values[0]

        try:
            df_games = week.groupby(['team', 'opponent']).apply(_get_game, week, i). \
                reset_index(drop=True). \
                drop_duplicates(). \
                reset_index(drop=True)
        except KeyError:
            breakpoint()

        df_games['week'] = [i] * len(df_games)

        return df_games

    games = data.groupby('file').apply(_to_name).reset_index([0, 1], drop=True)
    games = fix_postponed(games, league, season)

    games = games.groupby('week').apply(games_id_and_check, games, set(games.home.values))
    games.reset_index([0, 1], drop=True, inplace=True)
    games.drop(columns='index', inplace=True)
    games = score_and_points(games)
    games = games_new_attr(games)
    games = games.reindex(columns=GAMES_ATTRIB)

    return games


def add_opponent(df: pd.DataFrame):
    """

    :param df:
    :return:
    """
    from utils.constants import DEF_ATTRIB

    df.loc[:, 'enough_play'] = df.minutes > 75

    opps = []
    for i in range(len(df)):
        if not df.iloc[i].enough_play:
            opps.append(pd.Series({'opp_'+attr: 0 for attr in DEF_ATTRIB}))
            continue
        if df.iloc[i].position not in ['DR', 'DC', 'DL', 'DMC']:
            opps.append(pd.Series({'opp_' + attr: 0 for attr in DEF_ATTRIB}))
            continue

        df_opponent = df.query(f"week == {df.iloc[i].week} and team.str.contains('{df.iloc[i].opponent}')")
        df_opponent = df_opponent.loc[:, DEF_ATTRIB].rename(columns={attr: 'opp_'+attr for attr in DEF_ATTRIB}).sum()

        opps.append(df_opponent)

    df_opps = pd.concat(opps, axis=1).transpose()
    new_df = pd.concat([df, df_opps], axis=1, join='inner')

    return new_df


def enrich_players(league: str, season: str, games: pd.DataFrame, db: str = '../rotowire/database/Players.db',) -> pd.DataFrame:
    """
    This methods goes from a directory to a csv files that will be export.
    The directory should contains different stats per players among one season and as much csv as week played.
    The csv' name should finish i.csv where i corresponds to week.
    Moreover, since the attributes from rotowire are not explicit enough, we will use the dictionary ATTR_MEANING
    to make them more readable.
    The algorithm will also use the games data of the same league/season to add les id et nb attributes.
    Finally, the export csv is a concatenation of all the csv with new attributes names and the attribute 'week'.

    :param league: str. League names ('ligue1', 'bundesliga', 'premiere_league' ...).
    :param season: str. Season where the data is from in order to add it as an attribute.
    :param games: pd.Dataframe. Dataframe compute by compute_games for same league and season.
    :param db: str. Path to the database containing the games.
    :return: pd.Dataframe. Dataframe containing all the row of players with new attributes.
    """
    from utils.enrichment import add_games_id_for_players, players_new_attr2, players_id
    from utils.constants import DEF_ATTRIB
    logger.info(f'Running enrich_players for league : {league} and season : {season}')

    conn = sqlite3.connect(db)
    players = pd.read_sql_query(f'SELECT * FROM {league}_{season}', con=conn)

    players = players.groupby(['team', 'opponent', 'home_away']).apply(add_games_id_for_players, games)
    players = players_new_attr2(players)
    players = players_id(players)
    players = add_opponent(players)
    players = players.reindex(columns=PLAYERS_ATTRIB + ['opp_' + attr for attr in DEF_ATTRIB])
    players.sort_values(['week', 'id_player'], inplace=True)

    return players


def _player_summary(df):
    from utils.enrichment import summary_players_new_attr

    df_sum = df.drop(columns=['id_player', 'league', 'season', 'team', 'player_name', 'position'])
    df_sum = df_sum.sum()
    df_sum = summary_players_new_attr(df_sum)

    for attr in ['league', 'season', 'team', 'player_name']:
        df_sum[attr] = df.loc[:, attr].value_counts().index[0]

    pos = df.loc[:, 'position'].value_counts().index
    if pos[0] != 'SUB':
        df_sum['position'] = pos[0]
    elif pos[0] == 'SUB' and len(pos) > 1:
        df_sum['position'] = pos[1]
    else:
        df_sum['position'] = 'SUB'

    df_sum['played_games'] = len(df.query('minutes > 0'))

    return df_sum.to_frame().transpose()


def summarise_players(players: pd.DataFrame) -> pd.DataFrame:
    """

    :param players:
    :return:
    """
    from utils.constants import PLAY_ORIGINAL, SUMMARY_ATTRIB, DEF_ATTRIB

    players = players.loc[:, PLAY_ORIGINAL + ['opp_' + attr for attr in DEF_ATTRIB]]
    players_summary = players.groupby('id_player').apply(_player_summary)
    players_summary.reset_index(inplace=True)
    players_summary = players_summary.reindex(columns=SUMMARY_ATTRIB + ['opp_' + attr for attr in DEF_ATTRIB])

    return players_summary


def _home_summary(df):
    from utils.constants import H_GAME_ORIGINAL

    df_original = df.loc[:, H_GAME_ORIGINAL]
    df_original.rename(columns={s: '_'.join(s.split('_')[1:]) for s in df_original.keys()}, inplace=True)
    df_original = df_original.sum()
    df_original['nb_games'] = len(df)

    return df_original


def _away_summary(df):
    from utils.constants import A_GAME_ORIGINAL

    df_original = df.loc[:, A_GAME_ORIGINAL]
    df_original.rename(columns={s: '_'.join(s.split('_')[1:]) for s in df_original.keys()}, inplace=True)
    df_original = df_original.sum()
    df_original['nb_games'] = len(df)

    return df_original


def _all_summary(df):
    from utils.enrichment import players_new_attr

    df.drop(columns='index', inplace=True)
    df = df.sum()
    df = players_new_attr(df)

    return df


def summarise_teams(games: pd.DataFrame, league: str, season: str, nb_games: bool = False) -> pd.DataFrame:
    home = games.groupby('home').apply(_home_summary)
    away = games.groupby('away').apply(_away_summary)

    teams = pd.concat([home, away], sort=False)
    teams.reset_index(inplace=True)
    teams = teams.groupby(by='index').apply(_all_summary)
    teams['league'] = [league] * len(teams)
    teams['season'] = [season] * len(teams)
    if nb_games:
        teams = teams.reindex(columns=TEAMS_ATTRIB + ['nb_games'])
    else:
        teams = teams.reindex(columns=TEAMS_ATTRIB)
    teams.loc[:, 'goals_diff'] = teams.goals - teams.goals_conceded
    teams.sort_values(by=['points', 'goals_diff', 'goals'], ascending=False, inplace=True)
    teams.reset_index(inplace=True)
    teams.rename(columns={'index': 'team'}, inplace=True)

    return teams


def games_2sql(leagues: List[str], seasons: List[str], db: str = '../rotowire/database/GamesInfo.db',):
    """
    From all the csv of seasons and leagues, will computes the games and then concat it into one sql database.
    :param leagues: List[str]. All the desired league.
    :param seasons: List. All the desired season.
    :param db: str. Path to the database containing the games.
    :return: Export the sql database GamesInfo.db in rotowire/database.
    """

    conn = sqlite3.connect(db)
    c = conn.cursor()

    for league in leagues:
        for season in seasons:
            games = compute_games(league, season)
            games.to_sql(f'{league}_{season}', con=conn, if_exists='replace', index=False)


def excel_export(leagues: List[str], seasons: List[str]) -> None:
    """
    Given different leagues and seasons, will export one excel file containing all the data.
    :param leagues: List[str]. List of all leagues.
    :param seasons: List[str]. List of all seasons.
    :return: None. Will export the csv file.
    """
    logger.info(f'Exporting csv files for leagues : {leagues} and seasons : {seasons}')

    for league in leagues:
        for season in seasons:
            writer = pd.ExcelWriter(f'../excel_files/{league}_{season}.xlsx')

            games = compute_games(league, season)
            summary_games = summarise_teams(games, league, season)
            players = enrich_players(league, season, games)
            summary_players = summarise_players(players)

            breakpoint()

            games.to_excel(excel_writer=writer, sheet_name=f'games_{league}_{season}', index=False)
            players.to_excel(excel_writer=writer, sheet_name=f'players_{league}_{season}', index=False)
            summary_players.to_excel(excel_writer=writer, sheet_name=f'summary_players_{league}_{season}', index=False)
            summary_games.to_excel(excel_writer=writer, sheet_name=f'summary_teams_{league}_{season}', index=False)

            try:
                writer.save()
            except PermissionError:
                import os
                try:
                    os.remove(f'../excel_files/{league}_{season}.xlsx')
                except PermissionError:
                    logger.error('PermissionError : please close file and press c.')
                    breakpoint()
                    os.remove(f'../excel_files/{league}_{season}.xlsx')
                writer.save()


# games_2sql(['ligue1', 'prleague', 'liga'], ['1617', '1718', '1819', '1920'])
# players_2sql(['prleague'], ['2021'])
# excel_export(['ligue1'], ['2021'])

