from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from typing import List
import pandas as pd
import numpy as np
import sqlite3


def interpret_prediction(array):
    # TODO : improve this conversion 2-array float prediction to 2-array int representing [h_points, a_points]
    if array[0] > 1.8 and array[1] < 0.8:
        return [3, 0]
    elif array[1] > 1.8 and array[0] < 0.8:
        return [0, 3]
    else:
        return [1, 1]


def train_forest(leagues: List[str],
                 seasons: List[str],
                 test_size: float = 0.3,
                 db: str = 'rotowire/database/GamesInfo.db'):
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
         'a_%_big_chances_scored', 'a_shots_on_goal_inside_box', 'a_shots_on_goal'} | set([x for x in df.keys() if '%' in x])), inplace=True)
    df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

    train_features, test_features, train_labels, test_labels = \
        train_test_split(df, labels, test_size=test_size, random_state=42)

    rf = RandomForestRegressor(bootstrap=True, max_features='auto', min_samples_leaf=2,
                               min_samples_split=2, n_estimators=1800, max_depth=None)
    rf.fit(train_features, train_labels)

    h_predictions = [interpret_prediction(x)[0] for x in rf.predict(test_features)]
    a_predictions = [interpret_prediction(x)[1] for x in rf.predict(test_features)]
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


def custom_hyper_parameters(random_grid, train_features, train_labels):
    rf_estimator = RandomForestRegressor(n_estimators=1400, min_samples_split=2, min_samples_leaf=1,
                                         max_features='auto', max_depth=100, bootstrap=True)
    rf_random = RandomizedSearchCV(estimator=rf_estimator, param_distributions=random_grid, n_iter=100, cv=3, verbose=2,
                                   random_state=42, n_jobs=-1)
    rf_random.fit(train_features, train_labels)

    return rf_random.best_params_


# _, r, f = train_forest(['ligue1', 'prleague'], ['1617', '1718', '1819', '1920'])
# _, r1, f1 = train_forest(['ligue1'], ['1617', '1718', '1819', '1920'])
# _, r2, f2 = train_forest(['prleague'], ['1617'])

# breakpoint()

# print(r, f)
# print(r1, f1)
# print(r2, f2)
#
# breakpoint()

