def fix(df_fix, home: str, away: str, week: int):
    game = df_fix.query(f"id_home.str.contains('{home}') and id_away.str.contains('{away}')")
    row = list(game.index)[0]
    new_home = game.home.values[0]
    new_away = game.away.values[0]

    df_fix.loc[row, 'id_home'] = f'{week}_{new_home}'
    df_fix.loc[row, 'id_away'] = f'{week}_{new_away}'
    df_fix.loc[row, 'week'] = week

    return df_fix


def fix_postponed(df, league: str, season: str):
    if league == 'ligue1' and season == '1920':
        df = fix(df, 'Amiens', 'Reims', 16)
        df = fix(df, 'Monaco', 'Paris', 15)
        df = fix(df, 'Nimes', 'Rennes', 12)
        df = fix(df, 'Nimes', 'Rennes', 12)

    if league == 'ligue1' and season == '1819':
        df = fix(df, 'Angers', 'Bordeaux', 17)
        df = fix(df, 'Monaco', 'Nice', 17)
        df = fix(df, 'Nimes', 'Nantes', 17)
        df = fix(df, 'St_etienne', 'Marseille', 17)
        df = fix(df, 'Toulouse', 'Lyon', 17)
        df = fix(df, 'Paris', 'Montpellier', 17)
        df = fix(df, 'Amiens', 'Angers', 18)
        df = fix(df, 'Nantes', 'Montpellier', 18)
        df = fix(df, 'Guingamp', 'Rennes', 18)
        df = fix(df, 'Marseille', 'Bordeaux', 18)
        df = fix(df, 'Dijon', 'Paris', 18)
        df = fix(df, 'Caen', 'Toulouse', 18)
        df = fix(df, 'Bordeaux', 'Amiens', 19)
        df = fix(df, 'Nimes', 'Angers', 20)
        df = fix(df, 'Nantes', 'St_etienne', 22)
        df = fix(df, 'Caen', 'Nantes', 23)
        df = fix(df, 'St_etienne', 'Strasbourg', 23)
        df = fix(df, 'Bordeaux', 'Guingamp', 23)
        df = fix(df, 'Bordeaux', 'Montpellier', 27)
        df = fix(df, 'Nimes', 'Rennes', 27)
        df = fix(df, 'Nantes', 'Paris', 28)

    if league == 'ligue1' and season == '1718':
        df = fix(df, 'Amiens', 'Lille', 8)
        df = fix(df, 'Troyes', 'Dijon', 24)
        df = fix(df, 'Caen', 'Toulouse', 33)
        df = fix(df, 'Paris', 'Angers', 31)

    if league == 'ligue1' and season == '1617':
        df = fix(df, 'Metz', 'Lyon', 16)
        df = fix(df, 'Nantes', 'Caen', 17)
        df = fix(df, 'Caen', 'Nancy', 21)
        df = fix(df, 'Bastia', 'Nantes', 24)
        df = fix(df, 'Metz', 'Paris', 31)
        df = fix(df, 'Monaco', 'St_etienne', 31)
        df = fix(df, 'Toulouse', 'Marseille', 32)
        df = fix(df, 'St_etienne', 'Nantes', 32)
        df = fix(df, 'Paris', 'Guingamp', 32)
        df = fix(df, 'Nantes', 'Bordeaux', 33)
        df = fix(df, 'Bastia', 'Lyon', 33)
        df = fix(df, 'Marseille', 'St_etienne', 33)
        df = fix(df, 'Toulouse', 'Nice', 34)
        df = fix(df, 'St_etienne', 'Rennes', 34)
        df = fix(df, 'Lyon', 'Monaco', 34)
        df = fix(df, 'Caen', 'Marseille', 35)
        df = fix(df, 'Dijon', 'Bordeaux', 35)
        df = fix(df, 'Nice', 'Paris', 35)
        df = fix(df, 'Rennes', 'Montpellier', 36)
        df = fix(df, 'Lyon', 'Nantes', 36)
        df = fix(df, 'Marseille', 'Nice', 36)

        df = fix(df, 'Nantes', 'Guingamp', 37)
        df = fix(df, 'Montpellier', 'Lyon', 37)
        df = fix(df, 'Bordeaux', 'Marseille', 37)
        df = fix(df, 'Nice', 'Angers', 37)
        df = fix(df, 'Caen', 'Rennes', 37)
        df = fix(df, 'Bastia', 'Lorient', 37)
        df = fix(df, 'Dijon', 'Nancy', 37)
        df = fix(df, 'Monaco', 'Lille', 37)
        df = fix(df, 'St_etienne', 'Paris', 37)
        df = fix(df, 'Metz', 'Toulouse', 37)

    if league == 'prleague' and season == '1617':
        fix(df, 'Man_city', 'Man_united', 26)
        fix(df, 'Southampton', 'Arsenal', 26)

        fix(df, 'Middlesbrough', 'Sunderland', 28)
        fix(df, 'Arsenal', 'Leicester', 28)
        fix(df, 'Crystal_palace', 'Tottenham', 28)
        fix(df, 'Chelsea', 'Watford', 28)
        fix(df, 'Southampton', 'Man_united', 28)

        fix(df, 'Arsenal', 'Sunderland', 34)
        fix(df, 'Man_city', 'West_bromwich', 34)
        fix(df, 'Chelsea', 'Southampton', 34)
        fix(df, 'Leicester', 'Tottenham', 34)

    if league == 'prleague' and season == '1718':
        fix(df, 'Tottenham', 'West_ham', 21)
        fix(df, 'Burnley', 'Chelsea', 31)
        fix(df, 'Swansea', 'Southampton', 31)
        fix(df, 'Leicester', 'Arsenal', 31)
        fix(df, 'Tottenham', 'Newcastle', 31)
        fix(df, 'Man_city', 'Brighton', 31)
        fix(df, 'West_ham', 'Man_united', 31)
        fix(df, 'Chelsea', 'Huddersfield', 35)

    if league == 'prleague' and season == '1819':
        fix(df, 'Everton', 'Man_city', 27)
        fix(df, 'Chelsea', 'Brighton', 27)

        fix(df, 'Man_united', 'Man_city', 31)
        fix(df, 'Watford', 'Southampton', 31)
        fix(df, 'Brighton', 'Cardiff', 31)
        fix(df, 'Tottenham', 'Crystal_palace', 31)
        fix(df, 'Wolverhampthon', 'Arsenal', 31)

        fix(df, 'Tottenham', 'Brighton', 33)

    if league == 'prleague' and season == '1920':
        fix(df, 'West_ham', 'Liverpool', 18)
        # fix(df, 'Man_city', 'Arsenal', 28)
        # fix(df, 'Aston_villa', 'Sheffield_uni', 28)

    return df
