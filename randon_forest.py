from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np


# from build_database import get_games
# games = get_games(['ligue1'], ['1617', '1718', '1819', '1920'])


df = pd.read_pickle('last_games.pickle')
labels = df.loc[:, ['h_points', 'a_points']]
df.drop(columns=['h_points', 'a_points', 'id_home', 'id_away', 'nb_home', 'nb_away', 'league', 'season', 'week',
                 'file', 'home', 'away', 'score', 'h_formation'], inplace=True)
df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

train_features, test_features, train_labels, test_labels = \
    train_test_split(df, labels, test_size=0.3, random_state=42)

rf = RandomForestRegressor(n_estimators=1000, random_state=42)
rf.fit(train_features, train_labels)
predictions = rf.predict(test_features)

importances = list(rf.feature_importances_)

feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(df.keys(), importances)]
feature_importances = sorted(feature_importances, key=lambda x: x[1], reverse=True)
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]

breakpoint()
