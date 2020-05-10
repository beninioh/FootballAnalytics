def fix(df_fix, home: str, away: str, week: int):
    row = df_fix.query(f"id_home.str.contains('{home}') and id_away.str.contains('{away}')")
    row = list(row.index)[0]

    df_fix.loc[row, 'id_home'] = f'{week}_{home}'
    df_fix.loc[row, 'id_away'] = f'{week}_{away}'
    df_fix.loc[row, 'week'] = week

    return df_fix


def fix_postponed(df, league: str, season: str):
    if league == 'ligue1' and season == '1920':
        df = fix(df, 'amiens', 'reims', 16)
        df = fix(df, 'monaco', 'paris', 15)
        df = fix(df, 'nimes', 'rennes', 12)
        df = fix(df, 'nimes', 'rennes', 12)

    if league == 'ligue1' and season == '1819':
        df = fix(df, 'angers', 'bordeaux', 17)
        df = fix(df, 'monaco', 'nice', 17)
        df = fix(df, 'nimes', 'nantes', 17)
        df = fix(df, 'etienne', 'marseille', 17)
        df = fix(df, 'toulouse', 'lyon', 17)
        df = fix(df, 'paris', 'montpellier', 17)
        df = fix(df, 'amiens', 'angers', 18)
        df = fix(df, 'nantes', 'montpellier', 18)
        df = fix(df, 'guingamp', 'rennes', 18)
        df = fix(df, 'marseille', 'bordeaux', 18)
        df = fix(df, 'dijon', 'paris', 18)
        df = fix(df, 'caen', 'toulouse', 18)
        df = fix(df, 'bordeaux', 'amiens', 19)
        df = fix(df, 'nimes', 'angers', 20)
        df = fix(df, 'nantes', 'etienne', 22)
        df = fix(df, 'caen', 'nantes', 23)
        df = fix(df, 'etienne', 'strasbourg', 23)
        df = fix(df, 'bordeaux', 'guingamp', 23)
        df = fix(df, 'bordeaux', 'montpellier', 27)
        df = fix(df, 'nimes', 'rennes', 27)
        df = fix(df, 'nantes', 'paris', 28)

    if league == 'ligue1' and season == '1718':
        df = fix(df, 'amiens', 'lille', 8)
        df = fix(df, 'troyes', 'dijon', 24)
        df = fix(df, 'caen', 'toulouse', 33)
        df = fix(df, 'paris', 'angers', 31)

    if league == 'ligue1' and season == '1617':
        df = fix(df, 'metz', 'lyon', 16)
        df = fix(df, 'nantes', 'caen', 17)
        df = fix(df, 'caen', 'nancy', 21)
        df = fix(df, 'bastia', 'nantes', 24)
        df = fix(df, 'metz', 'paris', 31)
        df = fix(df, 'monaco', 'etienne', 31)
        df = fix(df, 'toulouse', 'marseille', 32)
        df = fix(df, 'etienne', 'nantes', 32)
        df = fix(df, 'paris', 'guingamp', 32)
        df = fix(df, 'nantes', 'bordeaux', 33)
        df = fix(df, 'bastia', 'lyon', 33)
        df = fix(df, 'marseille', 'etienne', 33)
        df = fix(df, 'toulouse', 'nice', 34)
        df = fix(df, 'etienne', 'rennes', 34)
        df = fix(df, 'lyon', 'monaco', 34)
        df = fix(df, 'caen', 'marseille', 35)
        df = fix(df, 'dijon', 'bordeaux', 35)
        df = fix(df, 'nice', 'paris', 35)
        df = fix(df, 'renne', 'montpellier', 36)
        df = fix(df, 'lyon', 'nantes', 36)
        df = fix(df, 'marseille', 'nice', 36)

        df = fix(df, 'nantes', 'guingamp', 37)
        df = fix(df, 'montpellier', 'lyon', 37)
        df = fix(df, 'bordeaux', 'marseille', 37)
        df = fix(df, 'nice', 'angers', 37)
        df = fix(df, 'caen', 'rennes', 37)
        df = fix(df, 'bastia', 'lorient', 37)
        df = fix(df, 'dijon', 'nancy', 37)
        df = fix(df, 'monaco', 'lille', 37)
        df = fix(df, 'etienne', 'paris', 37)
        df = fix(df, 'metz', 'toulouse', 37)

    return df
