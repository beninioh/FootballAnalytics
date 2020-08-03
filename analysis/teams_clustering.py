from utils.constants import TEAM_CLUSTER2
from utils.build_database import *
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from typing import List
import seaborn as sns
import pandas as pd
import numpy as np


def get_team(league: str, season: str, db: str = '../rotowire/database/GamesInfo.db'):
    """
    For a specific league and season, return the teams's stat for all the 20 teams at the end of the season.
    :param league: str. League's name.
    :param season: str. Season's name.
    :param db: str. Path to the database containing the games.
    :return: pd.DataFrame. Contains the teams values.
    """
    conn = sqlite3.connect(db)
    games = pd.read_sql_query(f'SELECT * FROM {league}_{season}', con=conn)
    teams = summarise_teams(games, league, season, nb_games=True)

    teams_int = teams.select_dtypes(include='float').divide(teams.nb_games, axis=0)
    teams.drop(columns=teams.select_dtypes(include='float').keys(), inplace=True)
    teams_normed = pd.concat([teams, teams_int], axis=1, sort=False).drop(columns=['nb_games'])

    return teams_normed


def get_teams(leagues: List[str], seasons: List[str], db: str = '../rotowire/database/GamesInfo.db',
              normalized: bool = True):
    """
    For different leagues and seasons, return the team's stat for all teams at the end of the season.
    :param leagues: List[str]. All the desired league.
    :param seasons: List. All the desired season.
    :param db: str. Path to the database containing the games.
    :param normalized: bool. True if the return data should be normalized.
    :return: pd.DataFrame. Contains the teams values.
    """
    teams = pd.concat([get_team(league, season, db) for league in leagues for season in seasons],
                      ignore_index=True, sort=False)
    teams_names = teams.team.values
    teams = teams.replace([np.inf, -np.inf, np.nan], 0).loc[:, TEAM_CLUSTER2].values

    if normalized:
        teams = normalized_teams(teams)

    return teams, teams_names


def normalized_teams(teams: List[np.ndarray]):
    teams_max = [np.nanmax(list(map(lambda x: x[i], teams))) for i in range(len(teams[0]))]
    teams_min = [np.nanmin(list(map(lambda x: x[i], teams))) for i in range(len(teams[0]))]

    teams_normed = []
    for team in teams:
        team_normed = [(team[i] - teams_min[i]) / (teams_max[i] - teams_min[i]) for i in range(len(teams[0]))]
        teams_normed.append(team_normed)

    return np.array(teams_normed)


def extract_score(array, a, b):
    if array[0] == a and array[1] == b:
        return array[2]


def get_cluster_tables(leagues: List[str], seasons: List[str], cluster: pd.DataFrame,
                       db: str = '../rotowire/database/GamesInfo.db'):
    """
    From different leagues and seasons, and a specific cluster pre-computed, would return the three cluster tables;
    corresponding to the interaction between cluster and asserting the likelihood from one team to win/draw/lose
    against another teams.
    The table size corresponds to the number of cluster. Ex : Team from cluster 1 playing against team from cluster 3.
    From the 3 tables, we can see the proportion of a win, a draw or a lose.
    :param leagues: List[str]. All the desired league.
    :param seasons: List. All the desired season.
    :param cluster: pd.DataFrame. Thanks to a pre-computed clustering, this would tell us which team is in which cluster.
    :param db: str. Path to the database containing the games.
    :return: List[pd.DataFrame]. Three data frame representing the likelihood of win/draw/lose.
    """
    cluster_infos = []
    conn = sqlite3.connect(db)
    games = pd.concat([pd.read_sql_query(f'SELECT * FROM {league}_{season}', con=conn)
                       for league in leagues
                       for season in seasons],
                      ignore_index=True, sort=False)
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


teams, _ = get_teams(['ligue1', 'prleague', 'liga'], ['1617', '1718', '1819', '1920'])

for perplex in range(5, 150, 5):
    tsne = TSNE(perplexity=perplex)
    X_embedded = tsne.fit_transform(teams)
    sns.scatterplot(X_embedded[:, 0], X_embedded[:, 1])
    plt.title(f'{perplex}')
    plt.show()

# for nb_clusters in range(4, 10):
#     kmeans = KMeans(n_clusters=nb_clusters, random_state=0).fit(X_embedded)
#
#     sns.scatterplot(X_embedded[:, 0], X_embedded[:, 1], hue=kmeans.labels_,
#                     palette=sns.color_palette("husl", len(set(kmeans.labels_))))
#     # sns.scatterplot(X_embedded[:, 0], X_embedded[:, 1])
#     plt.title(f'{nb_clusters}')
#     plt.show()

breakpoint()


cluster2 = pd.read_excel('clustering.xlsx')
t_win, t_draw, t_lose = get_cluster_tables(['ligue1', 'prleague', 'liga'], ['1617', '1718', '1819'], cluster2)

breakpoint()

