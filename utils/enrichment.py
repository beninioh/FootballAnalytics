def games_new_attr(df):
    df['h_%_goals_inside'] = df.h_goals_inside_box / df.h_goals * 100
    df['a_%_goals_inside'] = df.a_goals_inside_box / df.a_goals * 100
    df['h_%_goals_outside'] = df.h_goals_outside_box / df.h_goals * 100
    df['a_%_goals_outside'] = df.a_goals_outside_box / df.a_goals * 100
    df['h_%_goals_free_kick'] = df.h_free_kick_goals / df.h_goals * 100
    df['a_%_goals_free_kick'] = df.a_free_kick_goals / df.a_goals * 100
    df['h_%_goals_shot'] = df.h_shots / df.h_goals * 100
    df['a_%_goals_shot'] = df.a_shots / df.a_goals * 100
    df['h_%_goals_shot_on'] = df.h_shots_on_goal / df.h_goals * 100
    df['a_%_goals_shot_on'] = df.a_shots_on_goal / df.a_goals * 100
    df['h_%_shot_shot_on'] = df.h_shots_on_goal / df.h_shots * 100
    df['a_%_shot_shot_on'] = df.a_shots_on_goal / df.a_shots * 100
    df['h_%_goals_shot_inside'] = df.h_goals_inside_box / df.h_goals * 100
    df['a_%_goals_shot_inside'] = df.a_goals_inside_box / df.a_goals * 100
    df['h_%_shot_shot_inside'] = df.h_goals_inside_box / df.h_shots * 100
    df['a_%_shot_shot_inside'] = df.a_goals_inside_box / df.a_shots * 100
    df['h_%_goals_shot_on_inside'] = df.h_shots_on_goal_inside_box / df.h_goals * 100
    df['a_%_goals_shot_on_inside'] = df.a_shots_on_goal_inside_box / df.a_goals * 100
    df['h_%_shot_shot_on_inside'] = df.h_shots_on_goal_inside_box / df.h_shots * 100
    df['a_%_shot_shot_on_inside'] = df.a_shots_on_goal_inside_box / df.a_shots * 100
    df['h_%_goals_shot_outside'] = df.h_goals_outside_box / df.h_goals * 100
    df['a_%_goals_shot_outside'] = df.a_goals_outside_box / df.a_goals * 100
    df['h_%_shot_shot_outside'] = df.h_goals_outside_box / df.h_shots * 100
    df['a_%_shot_shot_outside'] = df.a_goals_outside_box / df.a_shots * 100
    df['h_%_goals_shot_on_outside'] = df.h_shots_on_goal_outside_box / df.h_goals * 100
    df['a_%_goals_shot_on_outside'] = df.a_shots_on_goal_outside_box / df.a_goals * 100
    df['h_%_shot_shot_on_outside'] = df.h_shots_on_goal_outside_box / df.h_shots * 100
    df['a_%_shot_shot_on_outside'] = df.a_shots_on_goal_outside_box / df.a_shots * 100
    df['h_%_assists_open_play'] = df.h_assists_from_open_play / df.h_assists * 100
    df['a_%_assists_open_play'] = df.a_assists_from_open_play / df.a_assists * 100
    df['h_%_assists_set_play'] = df.h_assists_from_set_play / df.h_assists * 100
    df['a_%_assists_set_play'] = df.a_assists_from_set_play / df.a_assists * 100
    df['h_%_goals_chances'] = df.h_chances_created / df.h_goals * 100
    df['a_%_goals_chances'] = df.a_chances_created / df.a_goals * 100
    df['h_%_goals_big_chances'] = df.h_big_chances_created / df.h_goals * 100
    df['a_%_goals_big_chances'] = df.a_big_chances_created / df.a_goals * 100
    df['h_%_chances_open_play'] = df.h_chances_created_from_open_play / df.h_chances_created * 100
    df['a_%_chances_open_play'] = df.a_chances_created_from_open_play / df.a_chances_created * 100
    df['h_%_chances_set_play'] = df.h_chances_created_from_set_play / df.h_chances_created * 100
    df['a_%_chances_set_play'] = df.a_chances_created_from_set_play / df.a_chances_created * 100
    df['h_%_big_chances_missed'] = df.h_big_chance_missed / df.h_big_chances_created * 100
    df['a_%_big_chances_missed'] = df.a_big_chance_missed / df.a_big_chances_created * 100
    df['h_%_big_chances_scored'] = df.h_big_chance_scored / df.h_big_chances_created * 100
    df['a_%_big_chances_scored'] = df.a_big_chance_scored / df.a_big_chances_created * 100
    df['h_%_touches_in_box'] = df.h_touches_in_box / df.h_touches * 100
    df['a_%_touches_in_box'] = df.a_touches_in_box / df.a_touches * 100
    df['h_%_passes_attempted'] = df.h_attempted_passes / df.h_passes * 100
    df['a_%_passes_attempted'] = df.a_attempted_passes / df.a_passes * 100
    df['h_%_passes_long_balls'] = df.h_accurate_long_balls / df.h_passes * 100
    df['a_%_passes_long_balls'] = df.a_accurate_long_balls / df.a_passes * 100
    df['h_%_passes_through_balls'] = df.h_accurate_through_balls / df.h_passes * 100
    df['a_%_passes_through_balls'] = df.a_accurate_through_balls / df.a_passes * 100
    df['h_%_crosses_accurate'] = df.h_accurate_crosses / df.h_crosses * 100
    df['a_%_crosses_accurate'] = df.a_accurate_crosses / df.a_crosses * 100
    df['h_%_touches_dribbles'] = df.h_dribbles / df.h_touches * 100
    df['a_%_touches_dribbles'] = df.a_dribbles / df.a_touches * 100
    df['h_%_dribbles_accurate'] = df.h_attempted_dribbles / df.h_dribbles * 100
    df['a_%_dribbles_accurate'] = df.a_attempted_dribbles / df.a_dribbles * 100
    df['h_%_touches_dispossessed'] = df.h_dispossessed / df.h_touches * 100
    df['a_%_touches_dispossessed'] = df.a_dispossessed / df.a_touches * 100
    df['h_%_fouls_yellow_cards'] = df.h_yellow_cards / df.h_fouls_committed * 100
    df['a_%_fouls_yellow_cards'] = df.a_yellow_cards / df.a_fouls_committed * 100

    return df


def id_and_check(df, df_games, teams):
    if len(set(df.home.values)) != 10:
        print(df.week.values[0], teams - set(df.home.values).union(set(df.away.values)))

    h = [
        f"""h_{1 + len(df_games.iloc[:i].query(f"id_home.str.contains('{df_games.home.values[i]}')"))}_{df_games.home.values[i]}"""
        for i in list(df.index)]
    a = [
        f"""a_{1 + len(df_games.iloc[:i].query(f"id_away.str.contains('{df_games.away.values[i]}')"))}_{df_games.away.values[i]}"""
        for i in list(df.index)]

    df['nb_home'] = h
    df['nb_away'] = a

    return df


