from .sqlite import Database
import json


class _SplitHistory:
    def add_not_commit(self, group_id, doer_id, lander_id, payer_ids, amount):
        Database.execute(
            '''insert into split_history
                (group_id, doer_id, lander_id, payer_ids, amount, created_at)
                values (?, ?, ?, ?, ?, now)''',
            group_id, doer_id, lander_id,
            json.dumps(payer_ids), amount)

    def list(self, group_id):
        history = Database.fetch(
            '''select created_at as timestamp, amount,
            doer_id, lander_id, payer_ids
                from split_history
                where group_id = ?
                order by created_at desc''',
            group_id)
        for history_entry in history:
            history_entry['payer_ids'] = json.loads(history_entry['payer_ids'])
        return history


SplitHistory = _SplitHistory()
