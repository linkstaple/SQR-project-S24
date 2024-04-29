import json
import sqlite3
import time
from unittest.mock import call

import pytest
import sys

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_add_not_commit_no_error(mocker):
    sys.path.append('src/')

    def side_eff(*args, **kwargs):
        return "AAAA"

    execute = mocker.patch(
        'src.db.sqlite.Database.execute',
        side_effect=side_eff
    )

    import src.db.split_history

    group_id, doer_id, lander_id, payer_ids, amount = 1, 2, 3, [1, 2], 100

    try:
        (src.db.split_history.SplitHistory.
         add_not_commit(group_id, doer_id, lander_id, payer_ids, amount))
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call('''insert into split_history
                (group_id, doer_id, lander_id, payer_ids, amount, created_at)
                values (?, ?, ?, ?, ?, time('now'))'''
             , 1, 2, 3, '[1, 2]', 100)
    ])


@pytest.mark.asyncio
async def test_add_not_commit_no_error(mocker):
    sys.path.append('src/')

    now = time.time()
    def side_eff(*args, **kwargs):
        return [{
            'created_at': now,
            'amount': 100,
            'doer_id': 1,
            'lander_id': 2,
            'payer_ids': json.dumps([1,2,3]),
        },{
            'created_at': now,
            'amount': 100,
            'doer_id': 1,
            'lander_id': 2,
            'payer_ids': json.dumps([1,2,3]),
        }]

    execute = mocker.patch(
        'src.db.sqlite.Database.fetch',
        side_effect=side_eff
    )

    import src.db.split_history

    group_id = 1

    try:
        assert (src.db.split_history.SplitHistory.
         list(group_id)) == [{
            'created_at': now,
            'amount': 100,
            'doer_id': 1,
            'lander_id': 2,
            'payer_ids': [1,2,3],
        },{
            'created_at': now,
            'amount': 100,
            'doer_id': 1,
            'lander_id': 2,
            'payer_ids': [1,2,3],
        }]
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call('''select strftime('%s', created_at) as timestamp, amount,
            doer_id, lander_id, payer_ids
                from split_history
                where group_id = ?
                order by created_at desc''',
             group_id)
    ])
