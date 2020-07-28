from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from typing import List
import pandas as pd
import numpy as np
import sqlite3


"""
This investigation is to extract what are the important features to win a football games; not including any 
attributes related to the goals (Otherwise easy and pointless). 
What came out after building a model based on games from 3 leagues (liga, ligue1 and pr league) during 4 seasons is :
Around 65 % accuracy and important mainly important features are : Big chance created, clearances and crosses.  
"""


def interpret_prediction(array):
    """
    From a random forest prediction array, usually a 2-size float in between 0 and 3 array,
    interpolate the return either [3, 0], [0,3] or [1,1].
    :param array: List[float].
    :return: List[int]
    """
    if array[0] > 1.8 and array[1] < 0.8:
        rs = [3, 0]
    elif array[1] > 1.8 and array[0] < 0.8:
        rs = [0, 3]
    else:
        rs = [1, 1]

    # print(array, rs)
    # breakpoint()
    return rs


def interpret_prediction2(array):
    """
    From a random forest prediction array, usually a 2-size float in between 0 and 3 array,
    compute the distance for the array to the three possible scrore and return either [3, 0], [0,3] or [1,1].
    In practice not really efficient.
    :param array: List[float].
    :return: List[int]
    """
    import math
    dist_h_win = math.sqrt((3 - array[0]) ** 2 + (0 - array[1]) ** 2)
    dist_a_win = math.sqrt((0 - array[0]) ** 2 + (3 - array[1]) ** 2)
    dist_draw = math.sqrt((1 - array[0]) ** 2 + (1 - array[1]) ** 2)

    if dist_h_win <= dist_a_win and dist_h_win <= dist_draw:
        return [3, 0]
    elif dist_a_win <= dist_h_win and dist_a_win <= dist_draw:
        return [0, 3]
    elif dist_draw <= dist_a_win and dist_draw <= dist_h_win:
        return [1, 1]
    else:
        raise ValueError('Algorithm should not experience the else case.')


def interpret_prediction3(array, max_dist=0.12578947368421053):
    """
    From a random forest prediction array, usually a 2-size float in between 0 and 3 array,
    interpolate using a max_dist parameter to return either [3, 0], [0,3] or [1,1].
    In practice the more efficient interpretation method ig the max_dist is proper tuned.
    :param array: List[float].
    :param max_dist: float. Represent the distance between array[0] and array[1] where the score will be interpret
    as a draw.
    :return: List[int]
    """
    if abs(array[0] - array[1]) < max_dist:
        rs = [1, 1]
    elif array[0] > array[1]:
        rs = [3, 0]
    else:
        rs = [0, 3]

    return rs


def train_forest(leagues: List[str],
                 seasons: List[str],
                 test_size: float = 0.3,
                 db: str = 'rotowire/database/GamesInfo.db',
                 interpret=interpret_prediction):
    """
    Providing games data, this method will fit a random forest in order to predict the issues of a game
    not including any attributes related to goals (otherwise too easy and pointless) such as : h_goals, h_assist ...
    :param leagues: List[str]. List of leagues to consider.
    :param seasons: List[str]. List of seasons to consider.
    :param test_size: float. Size of the test set (from 0 to 1)
    :param db: str. Path to the database containing the games.
    :param interpret: func. Function to interpret the prediction.
    :return: - Model build thanks to the random forest.
             - Accuracy of the model based on the test set.
             - Important features to predict the model.
    """
    conn = sqlite3.connect(db)
    df = pd.concat([pd.read_sql_query(f'SELECT * FROM {league}_{season}', con=conn)
                    for league in leagues for season in seasons], ignore_index=True, sort=False)

    labels = df.loc[:, ['h_points', 'a_points']]
    df.drop(columns=list(
        {'h_points', 'a_points', 'id_home', 'id_away', 'nb_home', 'nb_away', 'league', 'season', 'week', 'file', 'home',
         'away', 'score', 'h_formation', 'a_formation', 'h_goals', 'h_goals_conceded', 'h_goals_inside_box',
         'h_clean_sheets', 'h_%_goals_shot', 'h_%_goals_shot_on', 'h_%_shot_shot_outside', 'h_assist_own_goals',
         'h_goals_outside_box', 'h_%_goals_outside', 'h_%_goals_shot_on_inside', 'h_assists', 'h_%_shot_shot_inside',
         'h_errors_lead_to_goal', 'h_big_chance_scored', 'h_%_goals_inside', 'h_assists_from_open_play',
         'h_%_assist_chances', 'h_%_goals_shot_inside', 'h_%_assists_open_play', 'h_%_big_chances_scored',
         'h_%_assists_open_play', 'h_%_big_chances_scored', 'h_shots_on_goal_inside_box', 'h_shots_on_goal', 'a_goals',
         'a_goals_conceded', 'a_goals_inside_box', 'a_clean_sheets', 'a_%_goals_shot', 'a_%_goals_shot_on',
         'a_%_shot_shot_outside', 'a_assist_own_goals', 'a_goals_outside_box', 'a_%_goals_outside',
         'a_%_goals_shot_on_inside', 'a_assists', 'a_%_shot_shot_inside', 'a_errors_lead_to_goal',
         'a_big_chance_scored', 'a_%_goals_inside', 'a_assists_from_open_play', 'a_%_assist_chances',
         'a_%_goals_shot_inside', 'a_%_assists_open_play', 'a_%_big_chances_scored', 'a_%_assists_open_play',
         'a_%_big_chances_scored', 'a_shots_on_goal_inside_box', 'a_shots_on_goal'} | set(
            [x for x in df.keys() if '%' in x])), inplace=True)
    df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

    train_features, test_features, train_labels, test_labels = \
        train_test_split(df, labels, test_size=test_size, random_state=42)

    rf = RandomForestRegressor(n_estimators=2560, min_samples_split=3, min_samples_leaf=2, max_features=17,
                               max_depth=16, bootstrap=False)
    rf.fit(train_features, train_labels)

    h_predictions = [interpret(x)[0] for x in rf.predict(test_features)]
    a_predictions = [interpret(x)[1] for x in rf.predict(test_features)]
    predictions = pd.DataFrame({'h': np.subtract(h_predictions, test_labels.h_points),
                                'a': np.subtract(a_predictions, test_labels.a_points)})
    accuracy = predictions.h.value_counts().to_dict()[0] / len(predictions)

    importances = list(rf.feature_importances_)
    feature_importances = [(feature, importance, 2) for feature, importance in zip(df.keys(), importances)]
    feature_importances = sorted(feature_importances, key=lambda x: x[1], reverse=True)
    feature_importances = pd.DataFrame({x[0]: [x[1]] for x in feature_importances}).transpose()
    feature_importances['importances'] = feature_importances.loc[:, 0]
    feature_importances = feature_importances.drop(columns=0)
    imp_features = feature_importances.head(30)

    return rf, accuracy, imp_features


def custom_hyper_parameters(random_grid,
                            leagues: List[str],
                            seasons: List[str],
                            test_size: float = 0.3,
                            db: str = 'rotowire/database/GamesInfo.db'):
    """
    Providing different values for each hyper-parameters, will try randomly thanks to cross-correlation, what are
    the best combination of parameters.
    :param random_grid: Dict. For each hyper-parameters to tuned, a list of possible values.
    :param leagues: List[str]. List of leagues to consider.
    :param seasons: List[str]. List of seasons to consider.
    :param test_size: float. Size of the test set (from 0 to 1)
    :param db: str. Path to the database containing the games.
    :return: Dict. What seems to be the best hyper-parameter to consider.
    """
    conn = sqlite3.connect(db)
    df = pd.concat([pd.read_sql_query(f'SELECT * FROM {league}_{season}', con=conn)
                    for league in leagues for season in seasons], ignore_index=True, sort=False)

    labels = df.loc[:, ['h_points', 'a_points']]
    df.drop(columns=list(
        {'h_points', 'a_points', 'id_home', 'id_away', 'nb_home', 'nb_away', 'league', 'season', 'week', 'file', 'home',
         'away', 'score', 'h_formation', 'a_formation', 'h_goals', 'h_goals_conceded', 'h_goals_inside_box',
         'h_clean_sheets', 'h_%_goals_shot', 'h_%_goals_shot_on', 'h_%_shot_shot_outside', 'h_assist_own_goals',
         'h_goals_outside_box', 'h_%_goals_outside', 'h_%_goals_shot_on_inside', 'h_assists', 'h_%_shot_shot_inside',
         'h_errors_lead_to_goal', 'h_big_chance_scored', 'h_%_goals_inside', 'h_assists_from_open_play',
         'h_%_assist_chances', 'h_%_goals_shot_inside', 'h_%_assists_open_play', 'h_%_big_chances_scored',
         'h_%_assists_open_play', 'h_%_big_chances_scored', 'h_shots_on_goal_inside_box', 'h_shots_on_goal', 'a_goals',
         'a_goals_conceded', 'a_goals_inside_box', 'a_clean_sheets', 'a_%_goals_shot', 'a_%_goals_shot_on',
         'a_%_shot_shot_outside', 'a_assist_own_goals', 'a_goals_outside_box', 'a_%_goals_outside',
         'a_%_goals_shot_on_inside', 'a_assists', 'a_%_shot_shot_inside', 'a_errors_lead_to_goal',
         'a_big_chance_scored', 'a_%_goals_inside', 'a_assists_from_open_play', 'a_%_assist_chances',
         'a_%_goals_shot_inside', 'a_%_assists_open_play', 'a_%_big_chances_scored', 'a_%_assists_open_play',
         'a_%_big_chances_scored', 'a_shots_on_goal_inside_box', 'a_shots_on_goal'} | set(
            [x for x in df.keys() if '%' in x])), inplace=True)
    df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

    train_features, test_features, train_labels, test_labels = \
        train_test_split(df, labels, test_size=test_size, random_state=42)

    rf_estimator = RandomForestRegressor()
    rf_random = RandomizedSearchCV(estimator=rf_estimator, param_distributions=random_grid, n_iter=100, cv=3, verbose=2,
                                   random_state=42, n_jobs=-1)
    rf_random.fit(train_features, train_labels)

    return rf_random.best_params_


