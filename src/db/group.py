from .sqlite import Database
from .split_history import SplitHistory


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

    def list_users(self, user_id):
        groups = Database.fetch('''select groups_users.group_id as id, groups.name as name from groups_users
                        left join groups on groups_users.group_id = groups.id
                        where groups_users.user_id = $1''',
                                  user_id)
        return groups

    def get_members(self, group_id):
        members = Database.fetch('''select groups_users.user_id as id, users.username, groups_users.balance
        from groups_users 
        left join users on groups_users.user_id = users.id
        where groups_users.group_id = ?''',
                                 group_id)
        return members

    def add_transaction(self, group_id, doer_id, lander_id, payer_ids, amount):
        self._increase_balance_not_commit(group_id, lander_id, amount)
        for payer_id in payer_ids:
            self._increase_balance_not_commit(group_id, payer_id, -amount / len(payer_ids))
        SplitHistory.add_not_commit(group_id, doer_id, lander_id, payer_ids, amount)
        Database.commit()

    def _increase_balance_not_commit(self, group_id, user_id, increase):
        Database.execute('''update groups_users set balance = balance + ? where group_id = ? and user_id = ?''',
                         increase, group_id, user_id)


Group = _Group()
