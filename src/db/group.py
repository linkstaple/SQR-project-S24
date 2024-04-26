from model import model
from .sqlite import Database

class _Group():
    def get_user_groups(self, user_id) -> list[model.UserGroup]:
        response = (Database.
                execute('''select groups_users.group_id as id, groups.name as name from groups_users
                        left join groups on groups_users.group_id = groups.id
                        where groups_users.user_id = $1''',
                        user_id).
                fetchall())

        groups = list(map(model.UserGroup.model_validate, response))
        return groups

Group = _Group()
