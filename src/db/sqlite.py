import sqlite3

from config.config import Config
from model import model

class _Database():
    def __init__(self):
        self.connection = sqlite3.connect(Config.sqlite_path)
        with open(Config.sqlite_init_script_path, 'r') as init_db:
            self.connection.executescript(init_db.read())

        self.connection.commit()

    def __cursor(self):
        return sqlite3.connect(Config.sqlite_path).cursor()

    def query(self, query, *params):
        return self.__cursor().execute(query, params)

    def factory(self, cursor, row):
        fields = [column[0] for column in cursor.description]
        return {k: v for k, v in zip(fields, row)}

    def execute(self, query, *params):
        cursor = self.__cursor()
        cursor.row_factory = self.factory
        cursor.execute(query, params)
        cursor.connection.commit()
        return cursor

    def graceful_shutdown(self):
        self.connection.close()

Database = _Database()