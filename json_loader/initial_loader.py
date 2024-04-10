import psycopg
from pprint import pprint
from global_ import *

def init():
    setup_database()
    create_tables()
    return db_conn

# Creates database and creates global connection to it
def setup_database():
    try:
        with psycopg.connect(f'dbname=postgres user={db_username} password={db_password} host={db_host} port={db_port}', autocommit=True) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'DROP DATABASE IF EXISTS {db_name}')
                cursor.execute(f'CREATE DATABASE {db_name}')

        global db_conn
        db_conn = psycopg.connect(
                f'dbname={db_name} user={db_username} password={db_password} host={db_host} port={db_port}'
        )
    except psycopg.OperationalError as e:
        print('Failed to connect to database', e)
        exit(1)

def create_tables():
    with db_conn.cursor() as cursor:
        with open(os.path.join(dir_path, 'create_tables.sql')) as f:
            cursor.execute(f.read())