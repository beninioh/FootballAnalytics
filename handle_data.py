import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def add_points_and_ranking(df):
    df['draws'] = 38 - (df.wins + df.losses)
    df['points'] = 3 * df.wins + df.draws
    df['goals_diff'] = df.goals - df.goals_conceded

    def ranking(df_rank):
        df_ranked = df_rank.sort_values(by=['points', 'goals_diff', 'goals'], ascending=False)
        df_ranked['ranking'] = list(range(1, 21))
        return df_ranked.sort_values(by=['points', 'goals_diff', 'goals'], ascending=False)

    return df.groupby('season').apply(ranking)


def correlation(df):
    # sns.heatmap(abs(df.corr()))
    # plt.show()

    return df.corr().ranking


def mean(df):
    return df.mean()


df = pd.read_csv('premier_league/stats.csv')
# df = df.query("season in ['2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018']")

df = add_points_and_ranking(df)
# df.to_csv('stats_with_ranking.csv')

df = df.reset_index('season', drop=True)
df_correlation = df.groupby('season').apply(correlation)
# df_correlation.to_csv('seasons_correlation.csv')

df_correlation = df_correlation.mean().sort_values(ascending=False)
# df_correlation.to_csv('total_correlation.csv')

df_ranking_mean = df.groupby('ranking').apply(mean)
# df_ranking_mean.to_csv('ranking_mean.csv')
breakpoint()


