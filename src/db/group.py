from .sqlite import Database


class _Group:
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

    def get(self, group_id):
        rows = Database.fetch("select id, name from groups where id = $1", group_id)
        if len(rows) == 0:
            return None
        return rows[0]

    def list(self, user_id):
        groups = Database.fetch('''select groups_users.group_id as id, groups.name as name from groups_users
                        left join groups on groups_users.group_id = groups.id
                        where groups_users.user_id = $1''',
                                  user_id)
        return groups

    def get_members(self, group_id):
        members = Database.fetch('''select groups_users.user_id as id, users.username, 0 as dept
        from groups_users 
        left join users on groups_users.user_id = users.id
        where groups_users.group_id = ?''',
                                 group_id)
        return members

    def get_history(self, group_id):
        return []


Group = _Group()
