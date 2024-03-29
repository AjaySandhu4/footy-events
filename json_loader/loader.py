import psycopg
from pprint import pprint
# import sys
import os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))

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


def main():
    print(dir_path)
    pwd = os.environ['POSTGRES_PWD']
    setup_database('postgres', pwd)
    create_tables()
    insert_competitions()
    iterate_over_matches()
    db_conn.commit()
    # test_Q1()
    db_conn.close()

# Creates database 'a3' and creates global connection to it
def setup_database(user, pwd):
    try:
        with psycopg.connect(f'dbname=postgres user={user} password={pwd} host=localhost port=5432', autocommit=True) as conn:
            with conn.cursor() as cursor:
                cursor.execute('DROP DATABASE IF EXISTS project_test')
                cursor.execute('CREATE DATABASE project_test')

        global db_conn
        db_conn = psycopg.connect(
                f'dbname=project_test user={user} password={pwd} host=localhost port=5432'
        )
    except psycopg.OperationalError as e:
        print('Failed to connect to database', e)
        exit(1)

def create_tables():
    with db_conn.cursor() as cursor:
        with open(os.path.join(dir_path, 'create_tables.sql')) as f:
            cursor.execute(f.read())
        # cursor.execute('DROP TABLE IF EXISTS players')
        # cursor.execute('''
                    #    CREATE TABLE players 
                    #    (
                    #     player_id INTEGER PRIMARY KEY, 
                    #     player_name TEXT NOT NULL, 
                    #     team_name TEXT NOT NULL, 
                    #     jersey_number INT NOT NULL, 
                    #     country_name TEXT NOT NULL
                    #    );
        #                ''')
        # cursor.execute('DROP TABLE IF EXISTS shots')
        # cursor.execute(''' 
        #                 CREATE TABLE shots
        #                 (
        #                  event_id CHAR(36) PRIMARY KEY,
        #                  season_name CHAR(24) NOT NULL,
        #                  match_id INTEGER NOT NULL,
        #                  player_name TEXT NOT NULL,
        #                  xg DECIMAL NOT NULL
        #                 );
        #                 ''')
        # cursor.execute(''' 
        #                 DROP TABLE IF EXISTS players;
        #                 CREATE TABLE players 
        #                 (
        #                 player_id INTEGER PRIMARY KEY, 
        #                 player_name TEXT NOT NULL, 
        #                 team_name TEXT NOT NULL, 
        #                 jersey_number INT NOT NULL, 
        #                 country_name TEXT NOT NULL
        #                 );
        #                 DROP TABLE IF EXISTS shots;
        #                 CREATE TABLE shots
        #                 (
        #                  event_id CHAR(36) PRIMARY KEY,
        #                  season_name CHAR(24) NOT NULL,
        #                  match_id INTEGER NOT NULL,
        #                  player_name TEXT NOT NULL,
        #                  xg DECIMAL NOT NULL
        #                 );
        #                 ''')
        # cursor.execute(''' 
        #         CREATE TABLE shots
        #         (
        #             event_id TEXT PRIMARY KEY
        #         );
        #         ''')

def insert_competitions():
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

def iterate_over_matches():
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
                    load_season_data(os.path.join(competition_directory, season_file), season_name_by_season_id[season_id])

def load_season_data(season_file, season_name):
    print(season_name)
    f = open(season_file)

    season_data = json.load(f)

    for match in season_data:
        match_id = match['match_id']
        load_match_data(match)
        load_lineup_data(match_id) 
        load_event_data(match_id, season_name)
    f.close()

def load_match_data(match):
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

def load_lineup_data(match_id):
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


def load_event_data(match_id, season_name):
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
                    ball_out
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                event['id'], 
                match_id, 
                event['index'], 
                event['timestamp'], 
                event['period'],
                event['minute'], 
                event['second'], 
                event['type']['name'], 
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
                event.get('ball_out', None)
            ))
        if event_type in event_loaders:
            event_loaders[event_type](event['id'], event[event_type.lower()], match_id, season_name)



def load_shot(event_id, shot_event, match_id, season_name):
    with db_conn.cursor() as cursor:
        # cursor.execute('''INSERT INTO shot (event_id, match_id, season_name, player_name, xg) VALUES (%s, %s, %s, %s, %s);''', (shot_event['id'], match_id, season_name, shot_event['player']['name'], shot_event['shot']['statsbomb_xg']))
        cursor.execute('''
            INSERT INTO shot (
            event_id, 
            key_pass_id, 
            end_location_x, 
            end_location_y, 
            end_location_z, 
            aerial_won, 
            follows_dribble, 
            first_time, 
            open_goal, 
            statsbomb_xg, 
            deflected, 
            technique, 
            body_part, 
            shot_type, 
            outcome
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            event_id, 
            shot_event.get('key_pass_id'), 
            shot_event.get('end_location')[0] if shot_event.get('end_location') else None, 
            shot_event.get('end_location')[1] if shot_event.get('end_location') else None, 
            shot_event.get('end_location')[2] if shot_event.get('end_location') and len(shot_event.get('end_location')) > 2 else None, 
            shot_event.get('aerial_won'), 
            shot_event.get('follows_dribble'), 
            shot_event.get('first_time'), 
            shot_event.get('open_goal'), 
            shot_event.get('statsbomb_xg'), 
            shot_event.get('deflected'), 
            shot_event.get('technique', {}).get('name'), 
            shot_event.get('body_part', {}).get('name'), 
            shot_event.get('type', {}).get('name'), 
            shot_event.get('outcome', {}).get('name')
        ))

def testQ1():
    with db_conn.cursor() as cursor:
        cursor.execute('''SELECT player_name, AVG(xg) as avg_xg
            FROM shots
            WHERE season_name = 'La Liga 2020/2021'
            GROUP BY player_name
            ORDER BY avg_xg DESC; 
        ''')
        

event_loaders = {
    'Shot': load_shot
}

if __name__ == '__main__':
    main()