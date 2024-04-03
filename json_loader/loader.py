import psycopg
from pprint import pprint
# import sys
import os
import json
from initial_loader import *
from event_loaders import *

season_id_by_competition_id = {
    '2': ['44'],
    '11': ['4', '42', '90']
}

season_name_by_season_id = {
    '44': 'Premier League 2003/2004',
    '90': 'La Liga 2020/2021',
    '42': 'La Liga 2019/2020',
    '4': 'La Liga 2018/2019',
}

event_dict = {
    'Shot': {
        'loader': load_shot,
        'object_name': 'shot',
    },
    'Pass': {
        'loader': load_pass,
        'object_name': 'pass',
    },
    'Dribble': {
        'loader': load_dribble,
        'object_name': 'dribble',
    },
    'Bad Behaviour': {
        'loader': load_bad_behaviour,
        'object_name': 'bad_behaviour',
    },
    'Ball Receipt*': {
        'loader': load_ball_receipt,
        'object_name': 'ball_receipt',
    },
    'Ball Recovery': {
        'loader': load_ball_recovery,
        'object_name': 'ball_recovery',
    },
    'Block': {
        'loader': load_blocks,
        'object_name': 'block',
    },
    'Carry': {
        'loader': load_carry,
        'object_name': 'carry',
    },
    'Clearance': {
        'loader': load_clearance,
        'object_name': 'clearance',
    },
    'Duel': {
        'loader': load_duel,
        'object_name': 'duel',
    },
    'Foul Committed': {
        'loader': load_foul_committed,
        'object_name': 'foul_committed',
    },
    'Foul Won': {
        'loader': load_foul_won,
        'object_name': 'foul_won',
    },
    'Goal Keeper': {
        'loader': load_goalkeeper,
        'object_name': 'goalkeeper',
    },
    'Half End': {
        'loader': load_half_end,
        'object_name': 'half_end',
    },
    'Half Start': {
        'loader': load_half_start,
        'object_name': 'half_start',
    },
    'Injury Stoppage': {
        'loader': load_injury_stoppage,
        'object_name': 'injury_stoppage',
    },
    'Interception': {
        'loader': load_interception,
        'object_name': 'interception',
    },
    'Miscontrol': {
        'loader': load_miscontrol,
        'object_name': 'miscontrol',
    },
    'Player Off': {
        'loader': load_player_off,
        'object_name': 'player_off',
    },
    'Substitution': {
        'loader': load_substitution,
        'object_name': 'substitution',
    },
}


def main():
    db_conn = init()
    insert_competitions(db_conn)
    iterate_over_matches(db_conn)
    db_conn.commit()
    db_conn.close()


def insert_competitions(db_conn):
    with open(os.path.join(dir_path, 'open-data/data/competitions.json')) as competitions_file:
        competitions_data = json.load(competitions_file)
        with db_conn.cursor() as cursor:
            for competition in competitions_data:
                # pprint(competition)
                if (str(competition['competition_id']) in season_id_by_competition_id) and (str(competition['season_id']) in season_name_by_season_id):
                    pprint(competition)
                    cursor.execute('''
                        INSERT INTO competition (competition_id, season_id, competition_name, season_name, competition_country, competition_gender, competition_youth, competition_international)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    ''', 
                    (competition['competition_id'], 
                     competition['season_id'], 
                     competition['competition_name'], 
                     competition['season_name'], 
                     competition['country_name'], 
                     competition['competition_gender'],
                     competition['competition_youth'],
                     competition['competition_international']))

def iterate_over_matches(db_conn):
    print('Iterating over matches')
    directory = os.path.join(dir_path, 'open-data/data/matches')
    for competition_id in os.listdir(directory):
        print('competition_id',competition_id)
        competition_directory = os.path.join(directory, competition_id)
        if(competition_id in season_id_by_competition_id):
            for season_file in os.listdir(competition_directory):
                season_id = season_file.strip('.json')
                if season_id in season_id_by_competition_id[competition_id]:
                    print(season_id)
                    load_season_data(db_conn, os.path.join(competition_directory, season_file), season_name_by_season_id[season_id])

def load_season_data(db_conn, season_file, season_name):
    print(season_name)
    f = open(season_file)

    season_data = json.load(f)

    for match in season_data:
        match_id = match['match_id']
        load_match_data(db_conn, match)
        load_lineup_data(db_conn, match_id) 
        load_event_data(db_conn, match_id, season_name)
    f.close()

def load_match_data(db_conn, match):
    with db_conn.cursor() as cursor:
        cursor.execute('''INSERT INTO team (team_id, team_name, team_country) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;''', (match['home_team']['home_team_id'], match['home_team']['home_team_name'], match['home_team']['country']['name']))
        cursor.execute('''INSERT INTO team (team_id, team_name, team_country) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;''', (match['away_team']['away_team_id'], match['away_team']['away_team_name'], match['away_team']['country']['name']))
        cursor.execute('''
            INSERT INTO matches (match_id, competition_id, season_id, match_date, kick_off, stadium_name, stadium_country, referee_id, home_team_id, home_manager_id, home_score, away_team_id, away_manager_id, away_score, match_week, competition_stage)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        ''', 
        (
            match['match_id'],
            match['competition']['competition_id'],
            match['season']['season_id'], 
            match['match_date'], 
            match['kick_off'], 
            match['stadium']['name'] if 'stadium' in match else None,
            match['stadium']['country']['name'] if 'stadium' in match else None,
            match['referee']['id'] if 'referee' in match else None,
            match['home_team']['home_team_id'], 
            match['home_team']['managers'][0]['id'] if 'managers' in match['home_team'] and len(match['home_team']['managers']) > 0  else None,
            match['home_score'], 
            match['away_team']['away_team_id'], 
            match['away_team']['managers'][0]['id'] if 'managers' in match['away_team'] and len(match['away_team']['managers']) > 0  else None,
            match['away_score'], 
            match['match_week'],
            match['competition_stage']['name'],
        ))

def load_lineup_data(db_conn, match_id):
    print('Loading lineup')
    lineup_filename = os.path.join(dir_path, 'open-data/data/lineups', str(match_id)+'.json')
    f = open(lineup_filename)

    lineup_data = json.load(f)
    with db_conn.cursor() as cursor:
        for team in lineup_data:
            # print(team['team_name'])
            for player in team['lineup']:
                # print('\t'+player['player_name'])
                # cursor.execute('''INSERT INTO player VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;''', (player['player_id'], player['player_name'], team['team_name'], player['jersey_number'], player['country']['name']))
                cursor.execute('''INSERT INTO player VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;''', (player['player_id'], player['player_name'], player['player_nickname'], player['country']['name']))
    f.close()

def load_event_data(db_conn, match_id, season_name):
    # event_filename = os.path.join('/Users/ajay/Documents/COMP3005/project/open-data/data/events', str(match_id)+'.json')
    event_filename = os.path.join(dir_path, 'open-data/data/events', str(match_id)+'.json')
    f = open(event_filename)
    event_data = json.load(f)
    for event in event_data:
        event_type = event['type']['name']
        with db_conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO events (
                    event_id, 
                    match_id, 
                    event_index, 
                    event_timestamp, 
                    event_period,
                    event_minute, 
                    event_second, 
                    event_type, 
                    possession, 
                    possession_team_id,
                    play_pattern, 
                    team_id, 
                    player_id, 
                    position, 
                    location_x, 
                    location_y,
                    duration, 
                    under_pressure, 
                    off_camera, 
                    ball_out,
                    counterpress
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                event['id'], 
                match_id, 
                event['index'], 
                event['timestamp'], 
                event['period'],
                event['minute'], 
                event['second'], 
                event_type, 
                event['possession'],
                event['possession_team']['id'], 
                event['play_pattern']['name'], 
                event['team']['id'],
                event.get('player', {}).get('id'),
                event['position']['name'] if event.get('position') else None,
                event['location'][0] if event.get('location') else None,
                event['location'][1] if event.get('location') else None,
                event.get('duration', None), 
                event.get('under_pressure', None),
                event.get('off_camera', None), 
                event.get('ball_out', None),
                event.get('counterpress', None)
            ))
        if event_type in event_dict:
            event_dict[event_type]['loader'](db_conn, event['id'], event.get(event_dict[event_type]['object_name']) or {})

def testQ1():
    with db_conn.cursor() as cursor:
        # cursor.execute('''SELECT player_name, AVG(xg) as avg_xg
        #     FROM shots
        #     WHERE season_name = 'La Liga 2020/2021'
        #     GROUP BY player_name
        #     ORDER BY avg_xg DESC; 
        # ''')
        cursor.execute('''  
                            SELECT p.player_name, AVG(s.statsbomb_xg) as avg_xg
                            FROM shot s
                            INNER JOIN events e ON s.event_id = e.event_id
                            INNER JOIN player p ON e.player_id = p.player_id
                            INNER JOIN matches m ON e.match_id = m.match_id
                            INNER JOIN competition c ON m.competition_id = c.competition_id
                                    AND m.season_id = c.season_id
                            WHERE c.competition_name = 'La Liga' AND c.season_name = '2020/2021'
                            GROUP BY p.player_id
                            ORDER BY avg_xg DESC; 
                       ''')

if __name__ == '__main__':
    main()