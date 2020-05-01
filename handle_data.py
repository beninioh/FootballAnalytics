import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def add_points_and_ranking(df):
    points = []
    for i in range(len(df)):
        wins = df.loc[i, 'wins']
        draw = 38 - df.loc[i, 'wins'] + df.loc[i, 'losses']
        points.append(3*wins + draw)

    df['ranking'] = list(range(20)) * 12
    df['points'] = points

    return df


def correlation(df):
    # sns.heatmap(abs(df.corr()))
    # plt.show()

    return df.corr().classement


def mean(df):
    return df.mean()


df = pd.read_csv('premier_league/stats.csv')

df_correlation = df.groupby('season').apply(correlation)
df_correlation = df_correlation.mean().sort_values(ascending=False)

df_ranking_mean = df.groupby('classement').apply(mean)
breakpoint()


