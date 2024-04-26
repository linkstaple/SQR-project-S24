from .sqlite import Database


class _User:
    def list_users(self):
        return Database.execute("select id, username from users").fetchall()

    def register_user(self, username, hashed_password):
        Database.execute("insert into users (username, password) values ($1, $2)",
                         username, hashed_password).fetchall()

    def get_by_credentials(self, username, hashed_password):
        resp = (Database.
                execute("select id, username from users where username = $1 and password = $2",
                        username, hashed_password).
                fetchall())
        if resp is None or len(resp) == 0:
            return None
        return resp[0]

    def get_by_id(self, id):
        resp = (Database.
                execute("select id, username from users where id = $1",
                        id).
                    fetchall())
        if resp is None or len(resp) == 0:
            return None
        return resp[0]


User = _User()
