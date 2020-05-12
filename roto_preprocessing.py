from utils.constants import ATTR_MEANING, LIGUE1_TEAMS, GAMES_ATTRIB
from utils.enrichment import games_new_attr, games_id_and_check
from typing import List
import pandas as pd
import glob


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


def enrich_players(league: str, season: str):
    """
    This methods goes from a directory to a csv files that will be export.
    The directory should contains different stats per players among one season and as much csv as week played.
    The csv' name should finish i.csv where i corresponds to week.
    Moreover, since the attributes from rotowire are not explicit enough, we will use the dictionary ATTR_MEANING
    to make them more readable.
    Finally, the export csv is a concatenation of all the csv with new attributes names and the attribute 'week'.

    :param league: str. League names ('ligue1', 'bundesliga', 'premiere_league' ...).
    :param season: str. Wanted season ('1718', '1920' ...).
    :param season: str. Season where the data is from in order to add it as an attribute.
    :return: None. Will export the desired csv.
    """
    from utils.enrichment import players_id

    files_dir = glob.glob(f'rotowire/{league}/players/{season}/*.csv')
    files = get_files(files_dir)

    players = pd.concat([pd.read_csv(files[i]).rename(columns=ATTR_MEANING) for i in range(1, len(files) + 1)],
                        ignore_index=True, sort=False)

    players.loc[:, 'team'] = players.team.apply(lambda x: LIGUE1_TEAMS[x])
    players.loc[:, 'opponent'] = players.opponent.apply(lambda x: LIGUE1_TEAMS[x])

    players = players_id(players, league, season)


    # df.to_csv(f'rotowire/{league}/players/players_{league}_{season}.csv', index=False)


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
    files_dir = glob.glob(f'rotowire/{league}/players/{season}/*.csv')
    files = get_files(files_dir)

    weeks = []
    for i in range(1, len(files) + 1):
        week = pd.read_csv(files[i]).rename(columns=ATTR_MEANING)
        breakpoint()
        week['team'] = week.team.apply(lambda x: LIGUE1_TEAMS[x])
        week['opponent'] = week.opponent.apply(lambda x: LIGUE1_TEAMS[x])

        def get_game(df_team):
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
                                      'h_formation': [df_home.formation.unique()[0]],
                                      'a_formation': [df_away.formation.unique()[0]]})

            df_home.drop(columns=['player_name', 'team', 'opponent', 'home_away', 'formation', 'position',
                                  'games_played', 'minutes', 'starts', 'sub_on', 'sub_off'], inplace=True)
            df_away.drop(columns=['player_name', 'team', 'opponent', 'home_away', 'formation', 'position',
                                  'games_played', 'minutes', 'starts', 'sub_on', 'sub_off'], inplace=True)

            df_home.rename(columns={x: 'h_' + x for x in df_home.keys()}, inplace=True)
            df_away.rename(columns={x: 'a_' + x for x in df_away.keys()}, inplace=True)

            game = pd.concat([id_nb,
                              game_info,
                              df_home.sum().to_frame().transpose(),
                              df_away.sum().to_frame().transpose()],
                             axis=1, sort=False)

            return game

        games = week.groupby(['team', 'opponent']).apply(get_game).\
            reset_index(drop=True).\
            drop_duplicates().\
            reset_index(drop=True)

        games['week'] = [i] * len(games)

        weeks.append(games)

    df_games = pd.concat(weeks, ignore_index=True, sort=False)
    df_games = fix_postponed(df_games, league, season)
    df_games = df_games.groupby('week').apply(games_id_and_check, df_games, set(df_games.home.values))
    df_games = games_new_attr(df_games)
    df_games = df_games.reindex(columns=GAMES_ATTRIB)
    breakpoint()

    df_games.to_csv(f'rotowire/{league}/games/games_{league}_{season}.csv', index=False)


# players2games('ligue1', '1617')

enrich_players('ligue1', '1718')

