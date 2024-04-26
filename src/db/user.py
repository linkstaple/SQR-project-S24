from model import model
from .sqlite import Database

class _User():
    def list_users(self):
        return Database.query("select * from users").fetchall()

    def register_user(self, username, hashed_password):
        Database.execute("insert into users (username, password) values ($1, $2)",
                    username, hashed_password).fetchall()

    def get_user_by_credentials(self, username, hashed_password) -> model.User:
        resp = (Database.
                execute("select id, username from users where username = $1 and password = $2",
                        username, hashed_password).
                fetchall())
        if resp is None or len(resp) == 0:
            return None
        user = model.User.model_validate(resp[0])
        return user

User = _User()
