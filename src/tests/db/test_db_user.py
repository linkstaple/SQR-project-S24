import json
import sqlite3
from datetime import time
from unittest.mock import call

import pytest
import pytest_mock
import sys

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_list_users_no_error(mocker):
    sys.path.append('src/')

    def side_eff(*args, **kwargs):
        return "aaa"

    execute = mocker.patch(
        'src.db.sqlite.Database.fetch',
        side_effect=side_eff
    )

    import src.db.user

    try:
        assert src.db.user.User.list_users() == "aaa"
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call('select id, username from users'),
    ])


@pytest.mark.asyncio
async def test_register_user_no_error(mocker):
    sys.path.append('src/')

    execute = mocker.patch(
        'src.db.sqlite.Database.execute_and_commit',
    )

    import src.db.user

    try:
        assert src.db.user.User.register_user('u', 'p') is None
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call("insert into users (username, password) " +
             "values ($1, $2)",
             'u', 'p'),
    ])


@pytest.mark.asyncio
async def test_get_by_username_none_no_error(mocker):
    sys.path.append('src/')

    execute = mocker.patch(
        'src.db.sqlite.Database.fetch',
        return_value=None,
    )

    import src.db.user

    try:
        assert src.db.user.User.get_by_username('u') is None
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call("select id, username, password " +
             "from users where username = $1",
             'u'),
    ])


@pytest.mark.asyncio
async def test_get_by_username_empty_no_error(mocker):
    sys.path.append('src/')

    execute = mocker.patch(
        'src.db.sqlite.Database.fetch',
        return_value=[],
    )

    import src.db.user

    try:
        assert src.db.user.User.get_by_username('u') is None
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call("select id, username, password " +
             "from users where username = $1",
             'u'),
    ])


@pytest.mark.asyncio
async def test_get_by_username_no_error(mocker):
    sys.path.append('src/')

    execute = mocker.patch(
        'src.db.sqlite.Database.fetch',
        return_value=[{'id': '1'}],
    )

    import src.db.user

    try:
        assert src.db.user.User.get_by_username('u') == {'id': '1'}
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call("select id, username, password " +
             "from users where username = $1",
             'u'),
    ])


@pytest.mark.asyncio
async def test_get_by_id_none_no_error(mocker):
    sys.path.append('src/')

    execute = mocker.patch(
        'src.db.sqlite.Database.fetch',
        return_value=None,
    )

    import src.db.user

    try:
        assert src.db.user.User.get_by_id('u') is None
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call("select id, username from users where id = $1",
             'u'),
    ])


@pytest.mark.asyncio
async def test_get_by_id_empty_no_error(mocker):
    sys.path.append('src/')

    execute = mocker.patch(
        'src.db.sqlite.Database.fetch',
        return_value=[],
    )

    import src.db.user

    try:
        assert src.db.user.User.get_by_id('u') is None
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call("select id, username from users where id = $1",
             'u'),
    ])


@pytest.mark.asyncio
async def test_get_by_id_no_error(mocker):
    sys.path.append('src/')

    execute = mocker.patch(
        'src.db.sqlite.Database.fetch',
        return_value=[{'id': '1'}],
    )

    import src.db.user

    try:
        assert src.db.user.User.get_by_id('u') == {'id': '1'}
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call("select id, username from users where id = $1",
             'u'),
    ])


@pytest.mark.asyncio
async def test_user_exists_none_no_error(mocker):
    sys.path.append('src/')

    execute = mocker.patch(
        'src.db.sqlite.Database.fetch',
        return_value=None,
    )

    import src.db.user

    try:
        assert src.db.user.User.user_exists('u') == False
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call("select * from users where username = $1",
             'u'),
    ])


@pytest.mark.asyncio
async def test_user_exists_empty_no_error(mocker):
    sys.path.append('src/')

    execute = mocker.patch(
        'src.db.sqlite.Database.fetch',
        return_value=[],
    )

    import src.db.user

    try:
        assert src.db.user.User.user_exists('u') == False
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call("select * from users where username = $1",
             'u'),
    ])


@pytest.mark.asyncio
async def test_user_exists_no_error(mocker):
    sys.path.append('src/')

    execute = mocker.patch(
        'src.db.sqlite.Database.fetch',
        return_value=[{'id': '1'}],
    )

    import src.db.user

    try:
        assert src.db.user.User.user_exists('u') == True
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call("select * from users where username = $1",
             'u'),
    ])


@pytest.mark.asyncio
async def test_users_exist_less_users_no_error(mocker):
    sys.path.append('src/')

    def side_eff(*args, **kwargs):
        if args[1] == 1:
            return [[1]]
        if args[1] == 2:
            return [[1]]
        raise "unexpected input"

    execute = mocker.patch(
        'src.db.sqlite.Database.execute',
        side_effect=side_eff
    )

    import src.db.user

    try:
        assert src.db.user.User.users_exist([1, 2]) == False
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call('''select count (*) from users
                where id = ?''',
             1),
        call('''select count (*) from users
                where id = ?''',
             2),
    ])

@pytest.mark.asyncio
async def test_users_exist_less_users_no_error(mocker):
    sys.path.append('src/')

    def side_eff(*args, **kwargs):
        if args[1] == 1:
            return [[1]]
        if args[1] == 2:
            return [[0]]
        raise "unexpected input"

    execute = mocker.patch(
        'src.db.sqlite.Database.execute',
        side_effect=side_eff
    )

    import src.db.user

    try:
        assert src.db.user.User.users_exist([1, 2]) == False
    except TypeError as e:
        pytest.fail("Unexpected TypeError:", e)
    except sqlite3.OperationalError as e:
        pytest.fail("Unexpected sqlite3.OperationalError:", e)
    except Exception as e:
        pytest.fail("Unexpected exception: ", e)

    execute.assert_has_calls(calls=[
        call('''select count (*) from users
                where id = ?''',
             1),
        call('''select count (*) from users
                where id = ?''',
             2),
    ])
