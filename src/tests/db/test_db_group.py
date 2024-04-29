import json
import sqlite3
from datetime import time
from unittest.mock import call

import pytest
import pytest_mock
import sys

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_create_no_error(mocker):
    sys.path.append('src/')

    def side_eff(*args, **kwargs):
        print(args)
        if args[0] == "insert into groups (name) values ($1) returning id":
            return [[1]]

        return None

    execute = mocker.patch(
        'src.db.sqlite.Database.execute',
        side_effect=side_eff
    )

    commit = mocker.patch(
        'src.db.sqlite.Database.commit',
    )

    import src.db.group

    try:
        assert src.db.group.Group.create('1', [1, 2, 3]) == 1
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call('insert into groups (name) values ($1) returning id', '1'),
        call(f"insert into groups_users (group_id, user_id) " +
             f"values (?, ?),(?, ?),(?, ?)",
             1, 1, 1, 2, 1, 3),
    ])

    commit.assert_called()


@pytest.mark.asyncio
async def test_get_no_type_error(mocker: pytest_mock.mocker):
    sys.path.append('src/')

    fetch = mocker.patch(
        'src.db.sqlite.Database.fetch',
        return_value=[{"id": 1, "name": "aaa"}]
    )

    import src.db.group

    try:
        assert src.db.group.Group.get(1) == {"id": 1, "name": "aaa"}
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    fetch.assert_called_with("select id, name from groups where id = $1", 1)


@pytest.mark.asyncio
async def test_list_users_no_error(mocker: pytest_mock.mocker):
    sys.path.append('src/')

    fetch = mocker.patch(
        'src.db.sqlite.Database.fetch',
        return_value="aaa"
    )

    import src.db.group

    try:
        assert src.db.group.Group.list_users(1) == "aaa"
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        print(e)
        pytest.fail("Unexpected exception: ", e)

    fetch.assert_called_with('''select groups_users.group_id as id,
                groups.name as name from groups_users
                left join groups on groups_users.group_id = groups.id
                where groups_users.user_id = $1''',
                             1)


@pytest.mark.asyncio
async def test_get_members_no_type_error(mocker: pytest_mock.mocker):
    fetch = mocker.patch(
        'src.db.sqlite.Database.fetch',
        return_value=[{"id": 1, "name": "aaa"}]
    )

    import src.db.group

    try:
        assert src.db.group.Group.get_members(1), [{"id": 1, "name": "aaa"}]
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    fetch.assert_called_with('''select groups_users.user_id as id,
            users.username, groups_users.balance
        from groups_users
        left join users on groups_users.user_id = users.id
        where groups_users.group_id = ?''',
                             1)


@pytest.mark.asyncio
async def test_add_transaction_no_type_error(mocker: pytest_mock.mocker):
    execute = mocker.patch(
        'src.db.sqlite.Database.execute',
    )

    commit = mocker.patch(
        'src.db.sqlite.Database.commit',
    )

    import src.db.group

    try:
        src.db.group.Group.add_transaction(1, 1, 1, [1, 2], 100)
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call('''update groups_users
            set balance = balance + ? where group_id = ? and user_id = ?''',
             100, 1, 1),
        call('''update groups_users
            set balance = balance + ? where group_id = ? and user_id = ?''',
             -50, 1, 1),
        call('''update groups_users
            set balance = balance + ? where group_id = ? and user_id = ?''',
             -50, 1, 2),
        call('''insert into split_history
                (group_id, doer_id, lander_id, payer_ids, amount, created_at)
                values (?, ?, ?, ?, ?, now)''',
             1, 1, 1, json.dumps([1, 2]), 100)
    ])

    commit.assert_called()
