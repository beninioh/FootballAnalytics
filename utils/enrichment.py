from utils.logger import logger
import pandas as pd
import numpy as np


def games_new_attr(df: pd.DataFrame):
    df['h_%_goals_inside'] = df.h_goals_inside_box / df.h_goals
    df['a_%_goals_inside'] = df.a_goals_inside_box / df.a_goals 
    df['h_%_goals_outside'] = df.h_goals_outside_box / df.h_goals 
    df['a_%_goals_outside'] = df.a_goals_outside_box / df.a_goals 
    df['h_%_goals_free_kick'] = df.h_free_kick_goals / df.h_goals 
    df['a_%_goals_free_kick'] = df.a_free_kick_goals / df.a_goals 
    df['h_%_goals_shot'] = df.h_shots / df.h_goals 
    df['a_%_goals_shot'] = df.a_shots / df.a_goals 
    df['h_%_goals_shot_on'] = df.h_shots_on_goal / df.h_goals 
    df['a_%_goals_shot_on'] = df.a_shots_on_goal / df.a_goals 
    df['h_%_shot_shot_on'] = df.h_shots_on_goal / df.h_shots 
    df['a_%_shot_shot_on'] = df.a_shots_on_goal / df.a_shots 
    df['h_%_goals_shot_inside'] = df.h_goals_inside_box / df.h_goals 
    df['a_%_goals_shot_inside'] = df.a_goals_inside_box / df.a_goals 
    df['h_%_shot_shot_inside'] = df.h_goals_inside_box / df.h_shots 
    df['a_%_shot_shot_inside'] = df.a_goals_inside_box / df.a_shots 
    df['h_%_goals_shot_on_inside'] = df.h_shots_on_goal_inside_box / df.h_goals 
    df['a_%_goals_shot_on_inside'] = df.a_shots_on_goal_inside_box / df.a_goals 
    df['h_%_shot_shot_on_inside'] = df.h_shots_on_goal_inside_box / df.h_shots 
    df['a_%_shot_shot_on_inside'] = df.a_shots_on_goal_inside_box / df.a_shots 
    df['h_%_goals_shot_outside'] = df.h_goals_outside_box / df.h_goals 
    df['a_%_goals_shot_outside'] = df.a_goals_outside_box / df.a_goals 
    df['h_%_shot_shot_outside'] = df.h_goals_outside_box / df.h_shots 
    df['a_%_shot_shot_outside'] = df.a_goals_outside_box / df.a_shots 
    df['h_%_goals_shot_on_outside'] = df.h_shots_on_goal_outside_box / df.h_goals 
    df['a_%_goals_shot_on_outside'] = df.a_shots_on_goal_outside_box / df.a_goals 
    df['h_%_shot_shot_on_outside'] = df.h_shots_on_goal_outside_box / df.h_shots 
    df['a_%_shot_shot_on_outside'] = df.a_shots_on_goal_outside_box / df.a_shots 
    df['h_%_assists_open_play'] = df.h_assists_from_open_play / df.h_assists 
    df['a_%_assists_open_play'] = df.a_assists_from_open_play / df.a_assists 
    df['h_%_assists_set_play'] = df.h_assists_from_set_play / df.h_assists 
    df['a_%_assists_set_play'] = df.a_assists_from_set_play / df.a_assists 
    df['h_%_goals_chances'] = df.h_chances_created / df.h_goals 
    df['a_%_goals_chances'] = df.a_chances_created / df.a_goals 
    df['h_%_goals_big_chances'] = df.h_big_chances_created / df.h_goals 
    df['a_%_goals_big_chances'] = df.a_big_chances_created / df.a_goals 
    df['h_%_chances_open_play'] = df.h_chances_created_from_open_play / df.h_chances_created 
    df['a_%_chances_open_play'] = df.a_chances_created_from_open_play / df.a_chances_created 
    df['h_%_chances_set_play'] = df.h_chances_created_from_set_play / df.h_chances_created 
    df['a_%_chances_set_play'] = df.a_chances_created_from_set_play / df.a_chances_created 
    df['h_%_big_chances_missed'] = df.h_big_chance_missed / df.h_big_chances_created 
    df['a_%_big_chances_missed'] = df.a_big_chance_missed / df.a_big_chances_created 
    df['h_%_big_chances_scored'] = df.h_big_chance_scored / df.h_big_chances_created 
    df['a_%_big_chances_scored'] = df.a_big_chance_scored / df.a_big_chances_created 
    df['h_%_touches_in_box'] = df.h_touches_in_box / df.h_touches 
    df['a_%_touches_in_box'] = df.a_touches_in_box / df.a_touches 
    df['h_%_passes_attempted'] = df.h_attempted_passes / df.h_passes 
    df['a_%_passes_attempted'] = df.a_attempted_passes / df.a_passes 
    df['h_%_passes_long_balls'] = df.h_accurate_long_balls / df.h_passes 
    df['a_%_passes_long_balls'] = df.a_accurate_long_balls / df.a_passes 
    df['h_%_passes_through_balls'] = df.h_accurate_through_balls / df.h_passes 
    df['a_%_passes_through_balls'] = df.a_accurate_through_balls / df.a_passes 
    df['h_%_crosses_accurate'] = df.h_accurate_crosses / df.h_crosses 
    df['a_%_crosses_accurate'] = df.a_accurate_crosses / df.a_crosses 
    df['h_%_touches_dribbles'] = df.h_dribbles / df.h_touches 
    df['a_%_touches_dribbles'] = df.a_dribbles / df.a_touches 
    df['h_%_dribbles_accurate'] = df.h_attempted_dribbles / df.h_dribbles 
    df['a_%_dribbles_accurate'] = df.a_attempted_dribbles / df.a_dribbles 
    df['h_%_touches_dispossessed'] = df.h_dispossessed / df.h_touches 
    df['a_%_touches_dispossessed'] = df.a_dispossessed / df.a_touches 
    df['h_%_fouls_yellow_cards'] = df.h_yellow_cards / df.h_fouls_committed 
    df['a_%_fouls_yellow_cards'] = df.a_yellow_cards / df.a_fouls_committed

    df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    return df


def players_new_attr(df: pd.DataFrame):
    df['%_goals_inside'] = df.goals_inside_box / df.goals
    df['%_goals_outside'] = df.goals_outside_box / df.goals 
    df['%_goals_free_kick'] = df.free_kick_goals / df.goals 
    df['%_goals_shot'] = df.shots / df.goals 
    df['%_goals_shot_on'] = df.shots_on_goal / df.goals 
    df['%_shot_shot_on'] = df.shots_on_goal / df.shots 
    df['%_goals_shot_inside'] = df.goals_inside_box / df.goals 
    df['%_shot_shot_inside'] = df.goals_inside_box / df.shots 
    df['%_goals_shot_on_inside'] = df.shots_on_goal_inside_box / df.goals 
    df['%_shot_shot_on_inside'] = df.shots_on_goal_inside_box / df.shots 
    df['%_goals_shot_outside'] = df.goals_outside_box / df.goals 
    df['%_shot_shot_outside'] = df.goals_outside_box / df.shots 
    df['%_goals_shot_on_outside'] = df.shots_on_goal_outside_box / df.goals 
    df['%_shot_shot_on_outside'] = df.shots_on_goal_outside_box / df.shots 
    df['%_assists_open_play'] = df.assists_from_open_play / df.assists 
    df['%_assists_set_play'] = df.assists_from_set_play / df.assists 
    df['%_goals_chances'] = df.chances_created / df.goals 
    df['%_goals_big_chances'] = df.big_chances_created / df.goals 
    df['%_chances_open_play'] = df.chances_created_from_open_play / df.chances_created 
    df['%_chances_set_play'] = df.chances_created_from_set_play / df.chances_created 
    df['%_big_chances_missed'] = df.big_chance_missed / df.big_chances_created 
    df['%_big_chances_scored'] = df.big_chance_scored / df.big_chances_created 
    df['%_touches_in_box'] = df.touches_in_box / df.touches 
    df['%_passes_attempted'] = df.attempted_passes / df.passes 
    df['%_passes_long_balls'] = df.accurate_long_balls / df.passes 
    df['%_passes_through_balls'] = df.accurate_through_balls / df.passes 
    df['%_crosses_accurate'] = df.accurate_crosses / df.crosses 
    df['%_touches_dribbles'] = df.dribbles / df.touches 
    df['%_dribbles_accurate'] = df.attempted_dribbles / df.dribbles 
    df['%_touches_dispossessed'] = df.dispossessed / df.touches 
    df['%_fouls_yellow_cards'] = df.yellow_cards / df.fouls_committed

    df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    return df


def summary_players_new_attr(df: pd.DataFrame):
    df['%_goals_inside'] = df.goals_inside_box / df.goals if df.goals != 0 else 0
    df['%_goals_outside'] = df.goals_outside_box / df.goals if df.goals != 0 else 0
    df['%_goals_free_kick'] = df.free_kick_goals / df.goals if df.goals != 0 else 0
    df['%_goals_shot'] = df.shots / df.goals if df.goals != 0 else 0
    df['%_goals_shot_on'] = df.shots_on_goal / df.goals if df.goals != 0 else 0
    df['%_shot_shot_on'] = df.shots_on_goal / df.shots if df.shots != 0 else 0
    df['%_goals_shot_inside'] = df.goals_inside_box / df.goals if df.goals != 0 else 0
    df['%_shot_shot_inside'] = df.goals_inside_box / df.shots if df.shots != 0 else 0
    df['%_goals_shot_on_inside'] = df.shots_on_goal_inside_box / df.goals if df.goals != 0 else 0
    df['%_shot_shot_on_inside'] = df.shots_on_goal_inside_box / df.shots if df.shots != 0 else 0
    df['%_goals_shot_outside'] = df.goals_outside_box / df.goals if df.goals != 0 else 0
    df['%_shot_shot_outside'] = df.goals_outside_box / df.shots if df.shots != 0 else 0
    df['%_goals_shot_on_outside'] = df.shots_on_goal_outside_box / df.goals if df.goals != 0 else 0
    df['%_shot_shot_on_outside'] = df.shots_on_goal_outside_box / df.shots if df.shots != 0 else 0
    df['%_assists_open_play'] = df.assists_from_open_play / df.assists if df.assists != 0 else 0
    df['%_assists_set_play'] = df.assists_from_set_play / df.assists if df.assists != 0 else 0
    df['%_goals_chances'] = df.chances_created / df.goals if df.goals != 0 else 0
    df['%_goals_big_chances'] = df.big_chances_created / df.goals if df.goals != 0 else 0
    df['%_chances_open_play'] = df.chances_created_from_open_play / df.chances_created if df.chances_created != 0 else 0
    df['%_chances_set_play'] = df.chances_created_from_set_play / df.chances_created if df.chances_created != 0 else 0
    df['%_big_chances_missed'] = df.big_chance_missed / df.big_chances_created if df.big_chances_created != 0 else 0
    df['%_big_chances_scored'] = df.big_chance_scored / df.big_chances_created if df.big_chances_created != 0 else 0
    df['%_touches_in_box'] = df.touches_in_box / df.touches if df.touches != 0 else 0
    df['%_passes_attempted'] = df.attempted_passes / df.passes if df.passes != 0 else 0
    df['%_passes_long_balls'] = df.accurate_long_balls / df.passes if df.passes != 0 else 0
    df['%_passes_through_balls'] = df.accurate_through_balls / df.passes if df.passes != 0 else 0
    df['%_crosses_accurate'] = df.accurate_crosses / df.crosses if df.crosses != 0 else 0
    df['%_touches_dribbles'] = df.dribbles / df.touches if df.touches != 0 else 0
    df['%_dribbles_accurate'] = df.attempted_dribbles / df.dribbles if df.dribbles != 0 else 0
    df['%_touches_dispossessed'] = df.dispossessed / df.touches if df.touches != 0 else 0
    df['%_fouls_yellow_cards'] = df.yellow_cards / df.fouls_committed if df.fouls_committed != 0 else 0

    df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    return df


def games_id_and_check(df: pd.DataFrame, df_games: pd.DataFrame, teams: pd.DataFrame):
    if len(set(df.home.values)) != 10:
        print(df.week.values[0], teams - set(df.home.values).union(set(df.away.values)))

    df.reset_index(0, inplace=True)

    h = [
        f"""h_{1 + len(df_games.iloc[:i].query(f"id_home.str.contains('{df_games.home.values[i]}')"))}_{df_games.home.values[i]}"""
        for i in list(df.loc[:, 'index'].values)
        ]

    a = [
        f"""a_{1 + len(df_games.iloc[:i].query(f"id_away.str.contains('{df_games.away.values[i]}')"))}_{df_games.away.values[i]}"""
        for i in list(df.loc[:, 'index'].values)
        ]

    df['nb_home'] = h
    df['nb_away'] = a

    return df


def add_games_id_for_players(df: pd.DataFrame, df_games: pd.DataFrame):

    game = df_games.query(
            f"id_home.str.contains('{df.team.values[0]}') and id_away.str.contains('{df.opponent.values[0]}')"
                         )

    if game.empty:
        game = df_games.query(
            f"id_home.str.contains('{df.opponent.values[0]}') and id_away.str.contains('{df.team.values[0]}')"
                             )

    for id_nb in ('id_home', 'id_away', 'nb_home', 'nb_away'):
        try:
            df[id_nb] = list(game.loc[:, id_nb].unique()) * len(df)
        except ValueError:
            breakpoint()

    try:
        week = int(df.id_home.values[0][:2])
    except ValueError:
        week = int(df.id_home.values[0][:1])

    df['week'] = [week] * len(df)

    return df


def players_id(df_players: pd.DataFrame):

    teams = set(df_players.team.values).union(df_players.opponent.values)
    if len(teams) != 20:
        logger.error('Number of teams does not equal 20 !')

    players_dict = {}
    for team in teams:
        df_teams = df_players.query(f"team.str.contains('{team}')")
        players = df_teams.player_name.unique()

        players_dict = {**players_dict,
                        **{players[i-1]: f'{team}_{i}' for i in range(1, len(players) + 1)}}

    df_players['id_player'] = df_players.player_name.apply(lambda x: players_dict[x])

    return df_players


def _compute_point(row):
    if row.h_goals > row.a_goals:
        row['h_points'] = 3
        row['a_points'] = 0
    elif row.h_goals < row.a_goals:
        row['h_points'] = 0
        row['a_points'] = 3
    else:
        row['h_points'] = 1
        row['a_points'] = 1

    return row


def score_and_points(df: pd.DataFrame):
    df['score'] = df.h_goals.astype(str) + '-' + df.a_goals.astype(str)
    df = df.apply(lambda row: _compute_point(row), axis=1)

    return df
