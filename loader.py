import psycopg
from pprint import pprint
# import sys
import os
import json

season_id_by_competition_id = {
    '2': ['44'],
    '11': ['4', '42', '90']
}


def main():
    pwd = os.environ['POSTGRES_PWD']
    setup_database('postgres', pwd)
    create_tables()
    iterateOverMatches()
    
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
        table_creation = 'CREATE TABLE players (player_id NOT NULL, player_name TEXT NOT NULL, team_name TEXT NOT NULL, jersey_number INT NOT NULL, country_name TEXT NOT NULL);'
        cursor.execute('CREATE TABLE players (player_id INTEGER PRIMARY KEY, player_name TEXT NOT NULL, team_name TEXT NOT NULL, jersey_number INT NOT NULL, country_name TEXT NOT NULL);')

        db_conn.commit()

def iterateOverMatches():
    directory = '/Users/ajay/Documents/COMP3005/project/open-data/data/matches'
 
    for competition_id in os.listdir(directory):
        competition_directory = os.path.join(directory, competition_id)
        if(competition_id in season_id_by_competition_id):
            for season_file in os.listdir(competition_directory):
                season_id = season_file.strip('.json')
                if season_id in season_id_by_competition_id[competition_id]:
                    load_season(os.path.join(competition_directory, season_file))

def load_season(season_file):
    f = open(season_file)

    season_data = json.load(f)

    for match in season_data:
        match_id = match['match_id']
        load_lineup_data(match_id) 

    f.close()

def load_lineup_data(match_id):
    lineup_filename = os.path.join('/Users/ajay/Documents/COMP3005/project/open-data/data/lineups', str(match_id)+'.json')
    f = open(lineup_filename)

    lineup_data = json.load(f)
    with db_conn.cursor() as cursor:
        for team in lineup_data:
            print(team['team_name'])
            for player in team['lineup']:
                print('\t'+player['player_name'])
                # cursor.execute('INSERT INTO players (player_id, player_name, team_name, jersey_number, country_name)')
                cursor.execute('''INSERT INTO players VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING''', (player['player_id'], player['player_name'], team['team_name'], player['jersey_number'], player['country']['name']))
        db_conn.commit()
    f.close()






if __name__ == '__main__':
    main()