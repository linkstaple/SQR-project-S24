import model
from .sqlite import Database


class _Group:
    def get_user_groups(self, user_id) -> list[model.UserGroup]:
        response = Database.fetch('''select groups_users.group_id as id, groups.name as name from groups_users
                        left join groups on groups_users.group_id = groups.id
                        where groups_users.user_id = $1''',
                                  user_id)
        groups = list(map(model.UserGroup.model_validate, response))
        return groups

    def create(self, name, user_ids) -> int:
        [[id]] = Database.execute("insert into groups (name) values ($1) returning id", name)
        # say we are inserting users with ids 1, 2, 3 into group with id 10
        # the code below executes such sql:
        # insert into groups_users (group_id, user_id) values (?, ?),(?, ?),(?, ?)
        # with params (10, 1, 10, 2, 10, 3)
        relations = list(map(lambda user_id: (id, user_id), user_ids))
        Database.execute(f"insert into groups_users (group_id, user_id) values {','.join(['(?, ?)'] * len(relations))}",
                         *[x for xs in relations for x in xs])
        Database.commit()
        return id


Group = _Group()
