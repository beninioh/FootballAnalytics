from typing import List


def poisson_chances(xg_home: float, xg_away: float, n: int = 15, plot: bool = False):
    """
    Compute the chance of winning for both teams (home and away), and the chance of draw, based on the
    two total expected goals. The chance are computing using a Poisson distribution with expected goal as parameter.
    :param xg_home: float. Expected goals of the home team.
    :param xg_away: float. Expected goals of the away team.
    :param n: int. Maximum number of goal to consider.
    :param plot: bool. True if you want to plot the results.
    :return: List. List of the likelihood : home win, draw, away win.
    """
    from scipy.stats import poisson

    win_home, draft, win_away = 0, 0, 0

    for i in range(n):
        for j in range(n):
            if i == j:
                draft += poisson.pmf(i, xg_home) * poisson.pmf(i, xg_away)
            elif i < j:
                win_home += poisson.pmf(i, xg_home) * poisson.pmf(j, xg_away)
            else:
                win_away += poisson.pmf(i, xg_home) * poisson.pmf(j, xg_away)

    if plot:
        print('Chance of home win : ', win_home)
        print('Chance of draft : ', draft)
        print('Chance of home away : ', win_away)
        print('total sum : ', win_away + win_home + draft)

    return win_home, draft, win_away


# poisson_chances(1.53, 2.37, plot=True)


def get_std(array: List):
    """
    From an array corresponding to likelihoods, return the standard deviation based on the computation of the sum
    of the variance of the bernouilli distribution.
    :param array: List. List of likelihood.
    :return: float. The standard deviation.
    """
    from math import sqrt

    var = sum([x * (1-x) for x in array])
    return sqrt(var)


def normal_chances(xg_home: List[float], xg_away: List[float], n: int = 15, plot: bool = False):
    """
    Compute the chance of winning for both teams (home and away), and the chance of draw, based on the
    two list of expected goals. The chance are computing using a Normal distribution with mean of all expected goal
    and standard deviation as parameters.
    :param xg_home: List[float]. List of all the expected goals of the home team.
    :param xg_away: List[float]. List of all the expected goals of the away team.
    :param n: int. Maximum number of goal to consider.
    :param plot: bool. True if you want to plot the results.
    :return: List. List of the likelihood : home win, draw, away win.
    """
    # TODO understand why total sum does not equal to 1 (Seems more precise tho).

    from scipy.stats import norm
    import numpy as np

    normal_home = norm(loc=np.sum(xg_home), scale=get_std(xg_home))
    normal_away = norm(loc=np.sum(xg_away), scale=get_std(xg_away))

    win_home, draft, win_away = 0, 0, 0

    for i in range(n):
        for j in range(n):
            if i == j:
                draft += normal_home.pdf(i) * normal_away.pdf(i)
            elif i < j:
                win_home += normal_home.pdf(i) * normal_away.pdf(j)
            else:
                win_away += normal_home.pdf(i) * normal_away.pdf(j)

    if plot:
        print('Chance of home win : ', win_home)
        print('Chance of draft : ', draft)
        print('Chance of home away : ', win_away)
        print('total sum : ', win_away + win_home + draft)

    return win_home, draft, win_away


xg_home = [0.02, 0.02, 0.03, 0.04, 0.04, 0.05, 0.06, 0.07, 0.09, 0.1, 0.12, 0.13, 0.76]
xg_away = [0.01, 0.02, 0.02, 0.02, 0.03, 0.05, 0.05, 0.05, 0.06, 0.22, 0.30, 0.43, 0.48, 0.63]

# xg_home = [1/2] * 4
# xg_away = [1/6] * 12

poisson_chances(sum(xg_home), sum(xg_away), plot=True)
normal_chances(xg_home, xg_away, plot=True)


