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
    iterateOverMatches()
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
        cursor.execute('DROP TABLE IF EXISTS players')
        cursor.execute('''
                       CREATE TABLE players 
                       (
                        player_id INTEGER PRIMARY KEY, 
                        player_name TEXT NOT NULL, 
                        team_name TEXT NOT NULL, 
                        jersey_number INT NOT NULL, 
                        country_name TEXT NOT NULL
                       );
                       ''')
        cursor.execute('DROP TABLE IF EXISTS shots')
        cursor.execute(''' 
                        CREATE TABLE shots
                        (
                         event_id CHAR(36) PRIMARY KEY,
                         season_name CHAR(24) NOT NULL,
                         match_id INTEGER NOT NULL,
                         player_name TEXT NOT NULL,
                         xg DECIMAL NOT NULL
                        );
                        ''')
        # cursor.execute(''' 
        #         CREATE TABLE shots
        #         (
        #             event_id TEXT PRIMARY KEY
        #         );
        #         ''')

def iterateOverMatches():
    # directory = '/Users/ajay/Documents/COMP3005/project/open-data/data/matches'
    directory = os.path.join(dir_path, 'open-data/data/matches')
    print(directory)
 
    for competition_id in os.listdir(directory):
        competition_directory = os.path.join(directory, competition_id)
        if(competition_id in season_id_by_competition_id):
            for season_file in os.listdir(competition_directory):
                season_id = season_file.strip('.json')
                if season_id in season_id_by_competition_id[competition_id]:
                    load_season(os.path.join(competition_directory, season_file), season_name_by_season_id[season_id])

def load_season(season_file, season_name):
    # print(season_name)
    f = open(season_file)

    season_data = json.load(f)

    for match in season_data:
        match_id = match['match_id']
        load_lineup_data(match_id) 
        load_event_data(match_id, season_name)
    f.close()

def load_lineup_data(match_id):
    # lineup_filename = os.path.join('/Users/ajay/Documents/COMP3005/project/open-data/data/lineups', str(match_id)+'.json')
    lineup_filename = os.path.join(dir_path, 'open-data/data/lineups', str(match_id)+'.json')
    f = open(lineup_filename)

    lineup_data = json.load(f)
    with db_conn.cursor() as cursor:
        for team in lineup_data:
            # print(team['team_name'])
            for player in team['lineup']:
                # print('\t'+player['player_name'])
                cursor.execute('''INSERT INTO players VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;''', (player['player_id'], player['player_name'], team['team_name'], player['jersey_number'], player['country']['name']))
    f.close()


def load_event_data(match_id, season_name):
    # event_filename = os.path.join('/Users/ajay/Documents/COMP3005/project/open-data/data/events', str(match_id)+'.json')
    event_filename = os.path.join(dir_path, 'open-data/data/events', str(match_id)+'.json')
    f = open(event_filename)
    event_data = json.load(f)
    for event in event_data:
        event_type = event['type']['name']
        if event_type in event_loaders:
            event_loaders[event_type](event, match_id, season_name)



def load_shot(shot_event, match_id, season_name):
    # print('Loading shot')
    with db_conn.cursor() as cursor:
        # print('\t', type(shot_event['id']), type(shot_event['shot']['statsbomb_xg']))
        cursor.execute('''INSERT INTO shots (event_id, match_id, season_name, player_name, xg) VALUES (%s, %s, %s, %s, %s);''', (shot_event['id'], match_id, season_name, shot_event['player']['name'], shot_event['shot']['statsbomb_xg']))
        # cursor.execute('''INSERT INTO shots (id) VALUES (%s)''', (shot_event['id']))
        # db_conn.commit()

def testQ1():
    with db_conn.cursor() as cursor:
        cursor.execute('''SELECT SELECT player_name, AVG(xg) as avg_xg
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