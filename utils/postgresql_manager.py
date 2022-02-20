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
        #에러시 transaction 오류로 인해 autocommit으로 변경
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

        print(f"connnection established to {getenv('DB_HOST')}")

    def find(self, table_name, columns, conditions={}):
        columns = ', '.join(columns)
        conditions = ' AND '.join([
            key + ' = ' + '\'' + str(value) + '\'' if isinstance(value, str) else key + ' = ' + str(value)
            for key, value in conditions.items()])
        query = f"SELECT {columns} FROM {table_name} WHERE {conditions}" if conditions \
            else f"SELECT {columns} FROM {table_name}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def insert_one(self, table_name, data):
        keys = str(tuple(data.keys())).replace('\'', '')
        values = tuple(data.values())
        self.cursor.execute(f"INSERT INTO {table_name} {keys} VALUES {values}")
        self.connection.commit()

    def insert_many(self, table_name, data):
        if len(data) == 0:
            raise ValueError('`data` can not be an empty list.')

        for i in data :
            try :
                PostgresqlManager.insert_one(self, table_name, i)
            except Exception as e:
                print("Error with insert Review ",i)
                print("Error trace:", e)

    def __del__(self):
        self.connection.close()
        print('connection closed')
