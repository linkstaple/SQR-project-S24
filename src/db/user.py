from .sqlite import Database


class _User:
    def list_users(self):
        return Database.fetch("select id, username from users")

    def register_user(self, username, hashed_password):
        Database.execute_and_commit("insert into users (username, password) "
                                    "values ($1, $2)",
                                    username, hashed_password)

    def get_by_username(self, username):
        resp = Database.fetch("select id, username, password "
                              "from users where username = $1",
                              username)
        if resp is None or len(resp) == 0:
            return None
        return resp[0]

    def get_by_id(self, id):
        resp = Database.fetch("select id, username from users where id = $1",
                              id)
        if resp is None or len(resp) == 0:
            return None
        return resp[0]

    def user_exists(self, username):
        resp = Database.fetch("select * from users where username = $1",
                              username)

        return not (resp is None or len(resp) == 0)

    def users_exist(self, ids):
        [[count]] = Database.execute(
            f'''select count (*) from users
            where id in ({','.join(['?'] * len(ids))})''',
            *ids)
        return len(ids) == count


User = _User()
