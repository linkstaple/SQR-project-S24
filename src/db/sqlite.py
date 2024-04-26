import sqlite3

from model import model


class Database():

    def __init__(self):
        self.connection = sqlite3.connect('lazy_split.db')
        self.connection.execute('''
            create table if not exists users (
                id integer primary key,
                username text not null unique,
                password text not null
                )
        ''')

        self.connection.execute('''
            create table if not exists groups (
                id integer primary key,
                name text not null
                )
        ''')

        self.connection.execute('''
            create table if not exists groups_users (
                id integer primary key,
                group_id integer not null,
                user_id integer not null,
                amount integer not null
                )
        ''')

        self.connection.execute('''
            create table if not exists split_history (
                id integer primary key,
                group_id integer not null,
                lander_id integer not null,
                amount integer not null,
                payers text
                )
        ''')

        self.connection.commit()

    def new_db(self):
        return self

    def __cursor(self):
        return sqlite3.connect('lazy_split.db').cursor()

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

    def list_users(self):
        return self.query("select * from users").fetchall()

    def register_user(self, username, hashed_password):
        self.execute("insert into users (username, password) values ($1, $2)",
                    username, hashed_password).fetchall()

    def get_user_by_credentials(self, username, hashed_password) -> model.User:
        resp = (self.
                execute("select id, username from users where username = $1 and password = $2",
                        username, hashed_password).
                fetchall())
        print("adljfjkhsdkf", resp)
        if resp is None or len(resp) == 0:
            print('ok')
            return None
        user = model.User.model_validate(resp[0])
        return user

    def graceful_shutdown(self):
        self.connection.close()
