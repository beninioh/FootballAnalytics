from utils.constants import ATTR_MEANING, GAMES_ATTRIB, PLAYERS_ATTRIB, TEAMS, TEAMS_ATTRIB
from utils.enrichment import games_new_attr, games_id_and_check
from utils.logger import logger
from typing import List
import pandas as pd
import glob

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
        try:
            int(str(file)[-6])
            file_nbr = int(str(file)[-6:-4])
        except ValueError:
            file_nbr = int(str(file)[-5:-4])

        files[file_nbr] = file

    return files


def concat_csv(leagues: List[str], seasons: List[str]):
    """
    From all the csv of a season in a specific league, will concat into one csv with a file attribute.
    Moreover, the attributes names and the different teams are made more meaningful. And attributes league,
    season, week, file are add to make sql queries easier.
    Then a csv is export in the database repository and it needs to be added to google query.
    :param leagues: List[str]. All the desired league.
    :param seasons: List. All the desired season.
    :return: Export the csv to add to the bigquery bucket.
    """
    all_csv = []

    for league in leagues:
        for season in seasons:
            files_dir = glob.glob(f'rotowire/{league}/players/{season}/*.csv')
            files = get_files(files_dir)

            for i in range(1, len(files) + 1):
                csv = pd.read_csv(files[i]).rename(columns=ATTR_MEANING)
                csv['team'] = csv.team.apply(lambda x: TEAMS[league][x])
                csv['opponent'] = csv.opponent.apply(lambda x: TEAMS[league][x])

                csv['league'] = [league] * len(csv)
                csv['season'] = [season] * len(csv)
                csv['file'] = [i] * len(csv)

                all_csv.append(csv)

    df_csv = pd.concat(all_csv, ignore_index=True, sort=False)

    breakpoint()
    df_csv.to_csv(f'rotowire/database/players_{leagues[0]}_{seasons[0][:2] + seasons[-1][2:]}.csv', index=False)


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


def compute_games(league: str, season: str) -> pd.DataFrame:
    """
    This methods goes from a directory to a csv files that will be export.
    The directory should contains different stats per players among one season and as much csv as week played.
    The csv' name should finish i.csv where i corresponds to week.
    Moreover, since the attributes from rotowire are not explicit enough, we will use the dictionary ATTR_MEANING
    to make them more readable.
    The export csv represent all the df_games that has been happening during one season. Per df_games, different id are added,
    every attributes starting with h_ (a_) represent the home (away) team.

    :param league: str. League names ('ligue1', 'bundesliga', 'premiere_league' ...).
    :param season: str. Wanted season ('1718', '1920' ...).
    :return: pd.Dataframe. Dataframe with all the df_games for one season.
    """
    from utils.fix_postponed import fix_postponed
    from utils.enrichment import score_and_points
    from utils.query import get_data
    logger.info(f'Computing games for league : {league} and season : {season}')

    query = f"""
            SELECT *
            FROM football-basic-analysis.football.raw_players
            WHERE season = {season} and league = '{league}'
            """

    data = get_data(query)

    def _to_name(week):
        i = week.file.values[0]

        df_games = week.groupby(['team', 'opponent']).apply(_get_game, week, i). \
            reset_index(drop=True). \
            drop_duplicates(). \
            reset_index(drop=True)

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


def enrich_players(league: str, season: str, games: pd.DataFrame) -> pd.DataFrame:
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
    :return: pd.Dataframe. Dataframe containing all the row of players with new attributes.
    """
    from utils.enrichment import add_games_id_for_players, players_new_attr, players_id
    from utils.query import get_data
    logger.info(f'Running enrich_players for league : {league} and season : {season}')

    query = f"""
            SELECT *
            FROM football-basic-analysis.football.raw_players
            WHERE season = {season} and league = '{league}'
            """

    players = get_data(query)

    players = players.groupby(['team', 'opponent', 'home_away']).apply(add_games_id_for_players, games)
    players = players_new_attr(players)
    players = players_id(players)
    players = players.reindex(columns=PLAYERS_ATTRIB)
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
    from utils.constants import PLAY_ORIGINAL, SUMMARY_ATTRIB

    players = players.loc[:, PLAY_ORIGINAL]
    players_summary = players.groupby('id_player').apply(_player_summary)
    players_summary.reset_index(inplace=True)
    players_summary = players_summary.reindex(columns=SUMMARY_ATTRIB)

    return players_summary


def _home_summary(df):
    from utils.constants import H_GAME_ORIGINAL
    from utils.enrichment import players_new_attr

    df_original = df.loc[:, H_GAME_ORIGINAL]
    df_original.rename(columns={s: '_'.join(s.split('_')[1:]) for s in df_original.keys()}, inplace=True)
    df_original = df_original.sum()
    # df_original = players_new_attr(df_original)

    return df_original


def _away_summary(df):
    from utils.constants import A_GAME_ORIGINAL
    from utils.enrichment import players_new_attr

    df_original = df.loc[:, A_GAME_ORIGINAL]
    df_original.rename(columns={s: '_'.join(s.split('_')[1:]) for s in df_original.keys()}, inplace=True)
    df_original = df_original.sum()
    # df_original = players_new_attr(df_original)

    return df_original


def _all_summary(df):
    from utils.enrichment import players_new_attr

    df.drop(columns='index', inplace=True)
    df = df.sum()
    df = players_new_attr(df)

    return df


def summarise_teams(games: pd.DataFrame, league: str, season: str,) -> pd.DataFrame:
    home = games.groupby('home').apply(_home_summary)
    away = games.groupby('away').apply(_away_summary)

    teams = pd.concat([home, away], sort=False)
    teams.reset_index(inplace=True)
    teams = teams.groupby(by='index').apply(_all_summary)
    teams['league'] = [league] * len(teams)
    teams['season'] = [season] * len(teams)
    teams = teams.reindex(columns=TEAMS_ATTRIB)
    teams.sort_values(by='points', ascending=False, inplace=True)
    teams.reset_index(inplace=True)
    teams.rename(columns={'index': 'team'}, inplace=True)

    return teams


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
            writer = pd.ExcelWriter(f'excel_files/{league}_{season}.xlsx')

            games = compute_games(league, season)
            summary_games = summarise_teams(games, league, season)
            players = enrich_players(league, season, games)
            summary_players = summarise_players(players)

            games.to_excel(excel_writer=writer, sheet_name=f'games_{league}_{season}', index=False)
            players.to_excel(excel_writer=writer, sheet_name=f'players_{league}_{season}', index=False)
            summary_players.to_excel(excel_writer=writer, sheet_name=f'summary_players_{league}_{season}', index=False)
            summary_games.to_excel(excel_writer=writer, sheet_name=f'summary_teams_{league}_{season}', index=False)

            try:
                writer.save()
            except PermissionError:
                import os
                try:
                    os.remove(f'excel_files/{league}_{season}.xlsx')
                except PermissionError:
                    logger.error('PermissionError : please close file and press c.')
                    breakpoint()
                    os.remove(f'excel_files/{league}_{season}.xlsx')
                writer.save()

            breakpoint()


# concat_csv(['ligue1', 'prleague'], ['1617', '1718', '1819', '1920'])
# breakpoint()

excel_export(['ligue1', 'prleague'], ['1617', '1718', '1819', '1920'])
