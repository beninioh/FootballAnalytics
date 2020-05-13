ATTR_MEANING = {'GP': 'games_played', 'ST': 'starts', 'ON': 'sub_on', 'OFF': 'sub_off', 'MIN': 'minutes',
                'Y': 'yellow_cards', 'YR': 'yellow/red_cards', 'R': 'red_cards', 'G': 'goals', 'A': 'assists',
                'SA': 'secondary_assists', 'S': 'shots', 'SOG': 'shots_on_goal', 'INT': 'interceptions',
                'CR': 'crosses', 'ACR': 'accurate_crosses', 'CC': 'chances_created', 'BLK': 'blocks', 'TKL': 'tackles',
                'TKLW': 'tackles_won', 'FC': 'fouls_committed', 'FS': 'fouls_suffered', 'P': 'passes',
                'AP': 'attempted_passes', 'ACRO': 'accurate_crosses_open_play', 'AW': 'aerials_won',
                'BCC': 'big_chances_created', 'BR': 'ball_recoveries', 'DR': 'dribbles', 'DW': 'duels_won',
                'EG': 'errors_lead_to_goal', 'ES': 'errors_lead_to_shot', 'IBS': 'shots_inside_box',
                'IBSOG': 'shots_on_goal_inside_box', 'IBG': 'goals_inside_box', 'OBS': 'shots_outside_box',
                'OBSOG': 'shots_on_goal_outside_box', 'OBG': 'goals_outside_box', 'AOG': 'assist_own_goals',
                'APW': 'assist_penalties_won', 'DSP': 'dispossessed', 'OWN': 'own_goals', 'TOUCH': 'touches',
                'TBOX': 'touches_in_box', 'PK': 'penalty_kicks_taken', 'PKG': 'penalty_kick_goals',
                'PKM': 'penalty_kick_misses', 'PKSVD': 'penalty_kicks_saved', 'FKCR': 'free_kick_crosses',
                'FKACR': 'free_kick_accurate_crosses', 'CRN': 'corners', 'CRNCR': 'corner_crosses',
                'CRNW': 'corners_won', 'FKS': 'free_kick_shots', 'FKSOG': 'free_kick_shots_on_goal',
                'FKG': 'free_kick_goals', 'GC': 'goals_conceded', 'CS': 'clean_sheets', 'SV': 'saves',
                'IBSV': 'saves_from_shots_inside_box', 'OBSV': 'saves_from_shots_outside_box',
                'AKS': 'accurate_keeper_sweeper', 'PKC': 'penalty_kicks_conceded', 'PKF': 'penalties_faced',
                'PKSV': 'penalty_saves', 'CL': 'clearances', 'ECL': 'effective_clearances', 'PUNCH': 'punches',
                'ALB': 'accurate_long_balls', 'ATB': 'accurate_through_balls', 'LMT': 'last_man_tackle',
                'TOFF': 'total_offside', 'BCM': 'big_chance_missed', 'BCS': 'big_chance_scored',
                'ATTDR': 'attempted_dribbles', 'AOP': 'assists_from_open_play', 'ASP': 'assists_from_set_play',
                'CCOP': 'chances_created_from_open_play', 'CCSP': 'chances_created_from_set_play', 'Team': 'team',
                'OPP': 'opponent', 'H/A': 'home_away', 'Form': 'formation', 'Player Name': 'player_name',
                'POS': 'position'}

LIGUE_TO_ADD = ['gazelec_ajaccio']

LIGUE1_TEAMS = {'DIJ': 'Dijon', 'FCN': 'Nantes', 'ASM': 'Monaco', 'MTP': 'Montpellier', 'GUI': 'Guingamp',
                'ETI': 'St_etienne', 'TFC': 'Toulouse', 'PSG': 'Paris', 'SMC': 'Caen', 'FCM': 'Metz',
                'STR': 'Strasbourg', 'OL': 'Lyon', 'NO': 'Nimes', 'NIC': 'Nice', 'GDB': 'Bordeaux', 'SCO': 'Angers',
                'LIL': 'Lille', 'BRE': 'Brest', 'ASC': 'Amiens', 'OM': 'Marseille', 'REN': 'Rennes', 'SDR': 'Reims',
                'TRO': 'Troyes', 'BST': 'Bastia', 'FCL': 'Lorient', 'NAN': 'Nancy'}


GAMES_ATTRIB = ['id_home', 'id_away', 'nb_home', 'nb_away', 'home', 'away', 'week',
                
                'h_formation',
                'h_goals', 'h_goals_inside_box', 'h_%_goals_inside', 'h_goals_outside_box', 'h_%_goals_outside',
                'h_free_kick_goals', 'h_%_goals_free_kick', 'h_shots', 'h_%_goals_shot', 'h_shots_on_goal',
                'h_%_goals_shot_on', 'h_%_shot_shot_on', 'h_shots_inside_box', 'h_%_goals_shot_inside',
                'h_%_shot_shot_inside', 'h_shots_on_goal_inside_box', 'h_%_goals_shot_on_inside',
                'h_%_shot_shot_on_inside', 'h_shots_outside_box', 'h_%_goals_shot_outside', 'h_%_shot_shot_outside',
                'h_shots_on_goal_outside_box', 'h_%_goals_shot_on_outside', 'h_%_shot_shot_on_outside', 'h_blocks',
                'h_assists', 'h_secondary_assists', 'h_assists_from_open_play', 'h_%_assists_open_play',
                'h_assists_from_set_play', 'h_%_assists_set_play', 'h_assist_penalties_won', 'h_chances_created',
                'h_%_goals_chances', 'h_big_chances_created', 'h_%_goals_big_chances',
                'h_chances_created_from_open_play', 'h_%_chances_open_play', 'h_chances_created_from_set_play',
                'h_%_chances_set_play', 'h_big_chance_missed', 'h_%_big_chances_missed', 'h_big_chance_scored',
                'h_%_big_chances_scored', 'h_touches', 'h_touches_in_box', 'h_%_touches_in_box', 'h_attempted_passes',
                'h_passes', 'h_%_passes_attempted', 'h_accurate_long_balls', 'h_%_passes_long_balls',
                'h_accurate_through_balls', 'h_%_passes_through_balls', 'h_crosses', 'h_accurate_crosses',
                'h_%_crosses_accurate', 'h_accurate_crosses_open_play', 'h_attempted_dribbles', 'h_%_dribbles_accurate',
                'h_dribbles', 'h_%_touches_dribbles', 'h_dispossessed', 'h_%_touches_dispossessed', 'h_aerials_won',
                'h_duels_won', 'h_ball_recoveries', 'h_interceptions', 'h_tackles', 'h_tackles_won',
                'h_last_man_tackle', 'h_errors_lead_to_goal', 'h_errors_lead_to_shot', 'h_assist_own_goals',
                'h_own_goals', 'h_clearances', 'h_effective_clearances', 'h_fouls_committed', 'h_fouls_suffered',
                'h_yellow_cards', 'h_%_fouls_yellow_cards', 'h_yellow/red_cards', 'h_red_cards',
                'h_goals_conceded', 'h_clean_sheets', 'h_saves', 'h_saves_from_shots_inside_box',
                'h_saves_from_shots_outside_box', 'h_accurate_keeper_sweeper', 'h_punches',
                'h_total_offside', 'h_penalty_kicks_taken', 'h_penalty_kick_goals', 'h_penalty_kick_misses',
                'h_penalty_kicks_saved', 'h_free_kick_crosses', 'h_free_kick_accurate_crosses', 
                'h_free_kick_shots', 'h_free_kick_shots_on_goal', 'h_penalty_kicks_conceded', 'h_penalties_faced', 
                'h_penalty_saves', 'h_corners', 'h_corner_crosses', 'h_corners_won', 

                'a_formation',
                'a_goals', 'a_goals_inside_box', 'a_%_goals_inside', 'a_goals_outside_box', 'a_%_goals_outside',
                'a_free_kick_goals', 'a_%_goals_free_kick', 'a_shots', 'a_%_goals_shot', 'a_shots_on_goal',
                'a_%_goals_shot_on', 'a_%_shot_shot_on', 'a_shots_inside_box', 'a_%_goals_shot_inside',
                'a_%_shot_shot_inside', 'a_shots_on_goal_inside_box', 'a_%_goals_shot_on_inside',
                'a_%_shot_shot_on_inside', 'a_shots_outside_box', 'a_%_goals_shot_outside', 'a_%_shot_shot_outside',
                'a_shots_on_goal_outside_box', 'a_%_goals_shot_on_outside', 'a_%_shot_shot_on_outside', 'a_blocks',
                'a_assists', 'a_secondary_assists', 'a_assists_from_open_play', 'a_%_assists_open_play',
                'a_assists_from_set_play', 'a_%_assists_set_play', 'a_assist_penalties_won', 'a_chances_created',
                'a_%_goals_chances', 'a_big_chances_created', 'a_%_goals_big_chances',
                'a_chances_created_from_open_play', 'a_%_chances_open_play', 'a_chances_created_from_set_play',
                'a_%_chances_set_play', 'a_big_chance_missed', 'a_%_big_chances_missed', 'a_big_chance_scored',
                'a_%_big_chances_scored', 'a_touches', 'a_touches_in_box', 'a_%_touches_in_box', 'a_attempted_passes',
                'a_passes', 'a_%_passes_attempted', 'a_accurate_long_balls', 'a_%_passes_long_balls',
                'a_accurate_through_balls', 'a_%_passes_through_balls', 'a_crosses', 'a_accurate_crosses',
                'a_%_crosses_accurate', 'a_accurate_crosses_open_play', 'a_attempted_dribbles', 'a_%_dribbles_accurate',
                'a_dribbles', 'a_%_touches_dribbles', 'a_dispossessed', 'a_%_touches_dispossessed', 'a_aerials_won',
                'a_duels_won', 'a_ball_recoveries', 'a_interceptions', 'a_tackles', 'a_tackles_won',
                'a_last_man_tackle', 'a_errors_lead_to_goal', 'a_errors_lead_to_shot', 'a_assist_own_goals',
                'a_own_goals', 'a_clearances', 'a_effective_clearances', 'a_fouls_committed', 'a_fouls_suffered',
                'a_yellow_cards', 'a_%_fouls_yellow_cards', 'a_yellow/red_cards', 'a_red_cards',
                'a_goals_conceded', 'a_clean_sheets', 'a_saves', 'a_saves_from_shots_inside_box',
                'a_saves_from_shots_outside_box', 'a_accurate_keeper_sweeper', 'a_punches',
                'a_total_offside', 'a_penalty_kicks_taken', 'a_penalty_kick_goals', 'a_penalty_kick_misses',
                'a_penalty_kicks_saved', 'a_free_kick_crosses', 'a_free_kick_accurate_crosses', 
                'a_free_kick_shots', 'a_free_kick_shots_on_goal', 'a_penalty_kicks_conceded', 'a_penalties_faced', 
                'a_penalty_saves', 'a_corners', 'a_corner_crosses', 'a_corners_won']


PLAYERS_ATTRIB = ['id_player', 'player_name', 'id_home', 'id_away', 'team', 'opponent', 'week',
                
                  'formation',
                  'goals', 'goals_inside_box', '%_goals_inside', 'goals_outside_box', '%_goals_outside',
                  'free_kick_goals', '%_goals_free_kick', 'shots', '%_goals_shot', 'shots_on_goal',
                  '%_goals_shot_on', '%_shot_shot_on', 'shots_inside_box', '%_goals_shot_inside',
                  '%_shot_shot_inside', 'shots_on_goal_inside_box', '%_goals_shot_on_inside',
                  '%_shot_shot_on_inside', 'shots_outside_box', '%_goals_shot_outside', '%_shot_shot_outside',
                  'shots_on_goal_outside_box', '%_goals_shot_on_outside', '%_shot_shot_on_outside', 'blocks',
                  'assists', 'secondary_assists', 'assists_from_open_play', '%_assists_open_play',
                  'assists_from_set_play', '%_assists_set_play', 'assist_penalties_won', 'chances_created',
                  '%_goals_chances', 'big_chances_created', '%_goals_big_chances',
                  'chances_created_from_open_play', '%_chances_open_play', 'chances_created_from_set_play',
                  '%_chances_set_play', 'big_chance_missed', '%_big_chances_missed', 'big_chance_scored',
                  '%_big_chances_scored', 'touches', 'touches_in_box', '%_touches_in_box', 'attempted_passes',
                  'passes', '%_passes_attempted', 'accurate_long_balls', '%_passes_long_balls',
                  'accurate_through_balls', '%_passes_through_balls', 'crosses', 'accurate_crosses',
                  '%_crosses_accurate', 'accurate_crosses_open_play', 'attempted_dribbles', '%_dribbles_accurate',
                  'dribbles', '%_touches_dribbles', 'dispossessed', '%_touches_dispossessed', 'aerials_won',
                  'duels_won', 'ball_recoveries', 'interceptions', 'tackles', 'tackles_won',
                  'last_man_tackle', 'errors_lead_to_goal', 'errors_lead_to_shot', 'assist_own_goals',
                  'own_goals', 'clearances', 'effective_clearances', 'fouls_committed', 'fouls_suffered',
                  'yellow_cards', '%_fouls_yellow_cards', 'yellow/red_cards', 'red_cards',
                  'goals_conceded', 'clean_sheets', 'saves', 'saves_from_shots_inside_box',
                  'saves_from_shots_outside_box', 'accurate_keeper_sweeper', 'punches',
                  'total_offside', 'penalty_kicks_taken', 'penalty_kick_goals', 'penalty_kick_misses',
                  'penalty_kicks_saved', 'free_kick_crosses', 'free_kick_accurate_crosses', 
                  'free_kick_shots', 'free_kick_shots_on_goal', 'penalty_kicks_conceded', 'penalties_faced', 
                  'penalty_saves', 'corners', 'corner_crosses', 'corners_won']
