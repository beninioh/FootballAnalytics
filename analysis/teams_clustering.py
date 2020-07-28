from utils.build_database import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from utils.constants import TEAM_CLUSTER2
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans


def get_team(league, season, db: str = '../rotowire/database/GamesInfo.db'):
    conn = sqlite3.connect(db)
    games = pd.read_sql_query(f'SELECT * FROM {league}_{season}', con=conn)
    teams = summarise_teams(games, league, season)
    # teams.team = teams.team + f'_{league[:4]}_{season[:2]}'
    # teams_names = teams.team.values
    # teams = teams.replace([np.inf, -np.inf, np.nan], 0).loc[:, TEAM_CLUSTER2].values

    return teams


# teams = pd.concat([get_team(league, season) for league in ['ligue1', 'liga', 'prleague'] for season in ['1617', '1718', '1819']],
#                   ignore_index=True, sort=False)
# teams_names = teams.team.values
# teams = teams.replace([np.inf, -np.inf, np.nan], 0).loc[:, TEAM_CLUSTER2].values
#
# tsne = TSNE(perplexity=4)
# X_embedded = tsne.fit_transform(teams)
#
# for nb_clusters in range(4, 10):
#     kmeans = KMeans(n_clusters=nb_clusters, random_state=0).fit(X_embedded)
#
#     sns.scatterplot(X_embedded[:, 0], X_embedded[:, 1], hue=kmeans.labels_,
#                     palette=sns.color_palette("husl", len(set(kmeans.labels_))))
#     # sns.scatterplot(X_embedded[:, 0], X_embedded[:, 1])
#     plt.title(f'{nb_clusters}')
#     plt.show()
#
# breakpoint()

db: str = '../rotowire/database/GamesInfo.db'
conn = sqlite3.connect(db)
games = pd.concat([pd.read_sql_query(f'SELECT * FROM {league}_{season}', con=conn)
                   for league in ['ligue1', 'liga', 'prleague']
                   for season in ['1617', '1718', '1819']],
                  ignore_index=True, sort=False)

cluster = pd.read_excel('clustering.xlsx')


def extract_score(array, a, b):
    if array[0] == a and array[1] == b:
        return array[2]


def get_cluster_tables(games: pd.DataFrame, cluster: pd.DataFrame):
    cluster_infos = []
    for i in range(len(games)):
        game = games.iloc[i]
        home_cluster = \
        cluster.query(f"season == '{game.season}' and league == '{game.league}' and team == '{game.home}'") \
            .cluster.values[0]
        away_cluster = \
        cluster.query(f"season == '{game.season}' and league == '{game.league}' and team == '{game.away}'") \
            .cluster.values[0]

        cluster_infos.append((home_cluster, away_cluster, game.h_points))

    preds_w, preds_d, preds_l = [], [], []
    n = len(cluster.cluster.unique())

    for i in range(n):
        pred_w, pred_d, pred_l = [], [], []

        for j in range(n):
            scores = list(map(lambda x: extract_score(x, i, j), cluster_infos))
            n_scores = len([x for x in scores if x is not None])
            wins, draws, loses = scores.count(3) / n_scores, scores.count(1) / n_scores, scores.count(0) / n_scores

            pred_w.append(wins)
            pred_d.append(draws)
            pred_l.append(loses)

        preds_w.append(pred_w)
        preds_d.append(pred_d)
        preds_l.append(pred_l)

    df_w = pd.DataFrame(preds_w)
    df_d = pd.DataFrame(preds_d)
    df_l = pd.DataFrame(preds_l)

    return df_w, df_d, df_l


get_cluster_tables(games, cluster)

breakpoint()

