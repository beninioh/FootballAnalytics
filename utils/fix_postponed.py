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

    elif league == 'ligue1' and season == '1819':
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

    elif league == 'ligue1' and season == '1718':
        df = fix(df, 'Amiens', 'Lille', 8)
        df = fix(df, 'Troyes', 'Dijon', 24)
        df = fix(df, 'Caen', 'Toulouse', 33)
        df = fix(df, 'Paris', 'Angers', 31)

    elif league == 'ligue1' and season == '1617':
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

    elif league == 'prleague' and season == '1617':
        df = fix(df, 'Man_city', 'Man_united', 26)
        df = fix(df, 'Southampton', 'Arsenal', 26)

        df = fix(df, 'Middlesbrough', 'Sunderland', 28)
        df = fix(df, 'Arsenal', 'Leicester', 28)
        df = fix(df, 'Crystal_palace', 'Tottenham', 28)
        df = fix(df, 'Chelsea', 'Watford', 28)
        df = fix(df, 'Southampton', 'Man_united', 28)

        df = fix(df, 'Arsenal', 'Sunderland', 34)
        df = fix(df, 'Man_city', 'West_bromwich', 34)
        df = fix(df, 'Chelsea', 'Southampton', 34)
        df = fix(df, 'Leicester', 'Tottenham', 34)

    elif league == 'prleague' and season == '1718':
        df = fix(df, 'Tottenham', 'West_ham', 21)
        df = fix(df, 'Burnley', 'Chelsea', 31)
        df = fix(df, 'Swansea', 'Southampton', 31)
        df = fix(df, 'Leicester', 'Arsenal', 31)
        df = fix(df, 'Tottenham', 'Newcastle', 31)
        df = fix(df, 'Man_city', 'Brighton', 31)
        df = fix(df, 'West_ham', 'Man_united', 31)
        df = fix(df, 'Chelsea', 'Huddersfield', 35)

    elif league == 'prleague' and season == '1819':
        df = fix(df, 'Everton', 'Man_city', 27)
        df = fix(df, 'Chelsea', 'Brighton', 27)

        df = fix(df, 'Man_united', 'Man_city', 31)
        df = fix(df, 'Watford', 'Southampton', 31)
        df = fix(df, 'Brighton', 'Cardiff', 31)
        df = fix(df, 'Tottenham', 'Crystal_palace', 31)
        df = fix(df, 'Wolverhampthon', 'Arsenal', 31)

        df = fix(df, 'Tottenham', 'Brighton', 33)

    elif league == 'prleague' and season == '1920':
        df = fix(df, 'West_ham', 'Liverpool', 18)
        # fix(df, 'Man_city', 'Arsenal', 28)
        # fix(df, 'Aston_villa', 'Sheffield_uni', 28)

    elif league == 'liga' and season == '1617':
        # df = fix(df, 'Sevilla', 'Athletico_bilbao', 9)
        df = fix(df, 'Valencia', 'Real_madrid', 16)
        df = fix(df, 'Betis', 'Leganes', 17)
        df = fix(df, 'Athletico_madrid', 'Betis', 18)
        df = fix(df, 'Celta_vigo', 'Real_madrid', 21)
        df = fix(df, 'Celta_vigo', 'Real_madrid', 21)
        df = fix(df, 'Deportivo_Coruna', 'Betis', 21)
        df = fix(df, 'Celta_vigo', 'Las_palmas', 29)
        df = fix(df, 'Eibar', 'Las_palmas', 30)
        df = fix(df, 'Valencia', 'Celta_vigo', 30)
        df = fix(df, 'Real_Sociedad', 'Gijon', 31)
        df = fix(df, 'Alaves', 'Villarreal', 32)
        df = fix(df, 'Eibar', 'Athletico_madrid', 33)
        df = fix(df, 'Alaves', 'Eibar', 34)
        df = fix(df, 'Sevilla', 'Celta_vigo', 34)
        df = fix(df, 'Athletico_madrid', 'Betis', 34)
        df = fix(df, 'Malaga', 'Sevilla', 35)
        df = fix(df, 'Leganes', 'Betis', 36)

    elif league == 'liga' and season == '1718':
        df = fix(df, 'Leganes', 'Real_madrid', 16)
        df = fix(df, 'Barcelona', 'Villarreal',  34)
        df = fix(df, 'Sevilla', 'Real_madrid', 34)

    elif league == 'liga' and season == '1819':
        df = fix(df, 'Rayo_vallecano', 'Athletico_madrid', 3)
        df = fix(df, 'Villarreal', 'Real_madrid',  17)

    elif league == 'liga' and season == '1920':
        df = fix(df, 'Barcelona', 'Real_madrid', 10)
        df = fix(df, 'Eibar', 'Real_Sociedad', 24)

    return df
