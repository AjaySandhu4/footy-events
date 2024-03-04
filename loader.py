import psycopg
from pprint import pprint
import sys
import os


def main():
    pprint(sys.path)
    try:
        pwd = os.environ['POSTGRES_PWD']
        conn = psycopg.connect(
            f'dbname=University user=postgres password={pwd} host=localhost port=5432'
        )
    except psycopg.OperationalError as e:
        print(f'Error {e}')
        exit(1)
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM student")
        rows = cursor.fetchall()
        for row in rows:
            print(row)



if __name__ == '__main__':
    main()