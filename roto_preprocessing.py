from utils.constants import ATTR_MEANING, GAMES_ATTRIB, PLAYERS_ATTRIB, TEAMS
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
- players2games : From all the players of specific league / seasons, deduce games.
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
    df_csv.to_csv(f'rotowire/database/players_{leagues[0]}_{seasons[0][:2]+seasons[-1][2:]}.csv', index=False)


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
                              'week': [i]})

    df_home.drop(columns=['player_name', 'team', 'opponent', 'home_away', 'formation', 'position',
                          'games_played', 'minutes', 'starts', 'sub_on', 'sub_off',
                          'league', 'season', 'file'], inplace=True)
    df_away.drop(columns=['player_name', 'team', 'opponent', 'home_away', 'formation', 'position',
                          'games_played', 'minutes', 'starts', 'sub_on', 'sub_off',
                          'league', 'season', 'file'], inplace=True)

    df_home.rename(columns={x: 'h_' + x for x in df_home.keys()}, inplace=True)
    df_away.rename(columns={x: 'a_' + x for x in df_away.keys()}, inplace=True)

    game = pd.concat([id_nb,
                      game_info,
                      df_home.sum().to_frame().transpose(),
                      df_away.sum().to_frame().transpose()],
                     axis=1, sort=False)

    return game


def players2games(league: str, season: str):
    """
    This methods goes from a directory to a csv files that will be export.
    The directory should contains different stats per players among one season and as much csv as week played.
    The csv' name should finish i.csv where i corresponds to week.
    Moreover, since the attributes from rotowire are not explicit enough, we will use the dictionary ATTR_MEANING
    to make them more readable.
    The export csv represent all the games that has been happening during one season. Per games, different id are added,
    every attributes starting with h_ (a_) represent the home (away) team.

    :param league: str. League names ('ligue1', 'bundesliga', 'premiere_league' ...).
    :param season: str. Wanted season ('1718', '1920' ...).
    :return: None. However, export file with all the games for one season.
    """
    from utils.fix_postponed import fix_postponed
    from utils.query import get_data
    logger.info(f'Running players2games for league : {league} and season : {season}')

    query = f"""
            SELECT *
            FROM football-basic-analysis.football.raw_players
            WHERE season = {season} and league = '{league}'
            """

    data = get_data(query)

    def _to_name(week):
        i = week.file.values[0]

        games = week.groupby(['team', 'opponent']).apply(_get_game, week, i). \
            reset_index(drop=True). \
            drop_duplicates(). \
            reset_index(drop=True)

        games['week'] = [i] * len(games)

        return games

    df_games = data.groupby('file').apply(_to_name).reset_index([0, 1], drop=True)
    df_games = fix_postponed(df_games, league, season)

    df_games = df_games.groupby('week').apply(games_id_and_check, df_games, set(df_games.home.values))
    df_games.reset_index([0, 1], drop=True, inplace=True)
    df_games.drop(columns='index', inplace=True)
    df_games = games_new_attr(df_games)
    df_games = df_games.reindex(columns=GAMES_ATTRIB)

    breakpoint()
    df_games.to_csv(f'rotowire/{league}/games/games_{league}_{season}.csv', index=False)


def enrich_players(league: str, season: str):
    """
    This methods goes from a directory to a csv files that will be export.
    The directory should contains different stats per players among one season and as much csv as week played.
    The csv' name should finish i.csv where i corresponds to week.
    Moreover, since the attributes from rotowire are not explicit enough, we will use the dictionary ATTR_MEANING
    to make them more readable.
    The algorithm will also use the games data of the same league/season to add les id et nb attributes.
    Finally, the export csv is a concatenation of all the csv with new attributes names and the attribute 'week'.

    :param league: str. League names ('ligue1', 'bundesliga', 'premiere_league' ...).
    :param season: str. Wanted season ('1718', '1920' ...).
    :param season: str. Season where the data is from in order to add it as an attribute.
    :return: None. Will export the desired csv.
    """
    from utils.enrichment import games_id_for_players, players_new_attr, players_id
    from utils.query import get_data
    logger.info(f'Running enrich_players for league : {league} and season : {season}')

    query = f"""
            SELECT *
            FROM football-basic-analysis.football.raw_players
            WHERE season = {season} and league = '{league}'
            """

    players = get_data(query)

    players = games_id_for_players(players, league, season)
    players = players_new_attr(players)
    players = players_id(players)
    players = players.reindex(columns=PLAYERS_ATTRIB)

    players.to_csv(f'rotowire/{league}/players/players_{league}_{season}.csv', index=False)


# concat_csv(['ligue1', 'prleague'], ['1617', '1718', '1819', '1920'])
# breakpoint()

# for season in ['1920']:
#     players2games('prleague', season)
# breakpoint()

for season in ['1617', '1718', '1819', '1920']:
    for league in ['ligue1', 'prleague']:
        enrich_players(league, season)


