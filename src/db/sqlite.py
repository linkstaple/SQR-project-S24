import sqlite3


class Database():

    def __init__(self):
        self.connection = sqlite3.connect('lazy_split.db')
        self.connection.execute('''
            create table if not exists users (
                id integer primary key,
                username text not null,
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

    def list_users(self):
        return sqlite3.connect('lazy_split.db').cursor().execute("select * from users").fetchall()

    def graceful_shutdown(self):
        self.connection.close()
