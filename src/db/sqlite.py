import sqlite3
from config import Config


class _Database:
    def __init__(self):
        print('sqlite:', Config.sqlite_path)
        self.connection = sqlite3.connect(Config.sqlite_path)
        with open(Config.sqlite_init_script_path, 'r') as init_db:
            self.connection.executescript(init_db.read())

        self.connection.commit()

    def __factory(self, cursor, row):
        fields = [column[0] for column in cursor.description]
        return {k: v for k, v in zip(fields, row)}

    def fetch(self, query, *params):
        cursor = self.connection.cursor()
        cursor.row_factory = self.__factory
        cursor.execute(query, params)
        return cursor.fetchall()

    def execute(self, query, *params):
        return self.connection.execute(query, params).fetchall()

    def commit(self):
        return self.connection.commit()

    def execute_and_commit(self, query, *params):
        rows = self.connection.execute(query, params).fetchall()
        self.commit()
        return rows

    def graceful_shutdown(self):
        self.connection.close()


Database = _Database()
