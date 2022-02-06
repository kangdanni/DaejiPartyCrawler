import psycopg2
from dotenv import load_dotenv
from os.path import abspath, dirname, join
from os import getenv


BASE_DIR = abspath(dirname(dirname(__file__)))
dotenv_path = join(BASE_DIR, '.env')
load_dotenv(dotenv_path)


class PostgresqlManager:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=getenv('DB_HOST'), 
            dbname=getenv('DB_NAME'), 
            user=getenv('DB_USERNAME'),
            password=getenv('DB_PASSWORD'), 
            port=getenv('DB_PORT'))
        self.cursor = self.connection.cursor()

    def insert_one(self, table_name, data):
        keys = str(tuple(data.keys())).replace('\'', '')
        values = tuple(data.values()) 
        self.cursor.execute(f"INSERT INTO {table_name} {keys} VALUES {values}")
        self.connection.commit()

    def insert_many(self, table_name, data):
        if len(data) == 0:
            raise ValueError('`data` can not be an empty list.')
        keys = str(tuple(data[0].keys())).replace('\'', '')
        placeholders = ', '.join(['%s'] * len(data[0].keys()))
        query = f"INSERT INTO {table_name} {keys} VALUES ({placeholders})"
        values = [tuple(item.values()) for item in data]
        self.cursor.executemany(query, values)
        self.connection.commit()

