import psycopg
from pprint import pprint
from global_ import *

def init():
    pwd = os.environ['POSTGRES_PWD']
    setup_database('postgres', pwd)
    create_tables()
    return db_conn

# Creates database 'project_test' and creates global connection to it
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