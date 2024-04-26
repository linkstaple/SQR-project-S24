import sqlite3

from config.config import Config
from model import model


class Database():
    def __init__(self):
        self.connection = sqlite3.connect(Config.sqlite_path)
        with open(Config.sqlite_init_script_path, 'r') as init_db:
            self.connection.executescript(init_db.read())

        self.connection.commit()

    def new_db(self):
        return self

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
        if resp is None or len(resp) == 0:
            print('ok')
            return None
        user = model.User.model_validate(resp[0])
        return user

    def get_user_groups(self, user_id) -> list[model.UserGroup]:
        response = (self.
                execute('''select groups_users.group_id as id, groups.name as name from groups_users
                        left join groups on groups_users.group_id = groups.id
                        where groups_users.user_id = $1''',
                        user_id).
                fetchall())
        
        groups = list(map(model.UserGroup.model_validate, response))
        return groups

    def graceful_shutdown(self):
        self.connection.close()
