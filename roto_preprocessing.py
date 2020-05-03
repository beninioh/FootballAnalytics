from constants import ATTR_MEANING
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


def players_dir2csv(files_dir: List[str], final_csv: str, season: str):
    """
    This methods goes from a directory to a csv files that will be export.
    The directory should contains different stats per players among one season and as much csv as week played.
    The csv' name should finish i.csv where i corresponds to week.
    Moreover, since the attributes from rotowire are not explicit enough, we will use the dictionary ATTR_MEANING
    to make them more readable.
    Finally, the export csv is a concatenation of all the csv with new attributes names and the attribute 'week'.

    :param files_dir: List[str]. Directory where to find the csv per week played.
    :param final_csv: str. Name of the export csv.
    :param season: str. Season where the data is from in order to add it as an attribute.
    :return: None. Will export the desired csv.
    """
    files = get_files(files_dir)

    weeks = []
    for i in range(1, len(files) + 1):
        week = pd.read_csv(files[i]).rename(columns=ATTR_MEANING)

        try:
            week['home_away']
        except KeyError:
            raise ValueError('File does not seems to be of a proper format.')

        week['week'] = [i] * len(week)
        weeks.append(week)

    df = pd.concat(weeks, ignore_index=True, sort=False)
    df['season'] = season
    df.to_csv(final_csv)


def players2games(files_dir: List[str]):
    files = get_files(files_dir)

    weeks = []
    for i in range(1, len(files) + 1):
        week = pd.read_csv(files[i]).rename(columns=ATTR_MEANING)

        def get_game(df_team):
            df_opp = week.query(f"team == '{df_team.opponent.values[0]}'")

            sum_team = df_team.sum()
            sum_opp = df_opp.sum()

            if df_team.home_away.values[0] == 'H':
                df_home, df_away = df_team, df_opp
            elif df_team.home_away.values[0] == 'A':
                df_home, df_away = df_opp, df_team
            else:
                raise ValueError("A team cannot play neither home or away")

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

            game = pd.concat([game_info,
                              df_home.sum().to_frame().transpose(),
                              df_away.sum().to_frame().transpose()],
                             axis=1, sort=False)

            return game

        games = week.groupby('team').apply(get_game).reset_index(drop=True)
        games['week'] = [i] * len(games)

        weeks.append(games)

    df_games = pd.concat(weeks, ignore_index=True, sort=False).drop_duplicates()
    df_games.to_csv('games_ligue1_1920.csv')


fil_dir = glob.glob('rotowire/ligue1/players/1920/*.csv')
players2games(fil_dir)

# players_dir2csv(fil_dir, 'players_ligue1_1920.csv', '1920')

# fil_dir = glob.glob('rotowire/ligue1/ranking/*.csv')
# for file in fil_dir:
#     df = pd.read_csv(file).rename(columns=ATTR_MEANING)
#     df['season'] = int(str(file)[-8:-4])
#     breakpoint()
#     df.to_csv(file)
