import base64
import json
from http import HTTPStatus

import bcrypt
import jwt
import pytest
import pytest_mock

import sys

sys.path.append('src/')

from model import *
from config import Config


@pytest.fixture
def new_user() -> RegisterUser:
    """ returns new user without token """
    return RegisterUser(
        username="username",
        password="password",
    )


def test_get_all(mocker: pytest_mock.mocker, new_user):
    mocker.patch(
        'db.user.User.list_users',
        autospec=True,
        return_value=[{'id': 1, 'username': 'a'}],
    )
    import service.user
    resp = service.user.get_all()
    assert resp.status_code == 200
    assert json.loads(resp.body.decode())['users'][0]['id'] == 1
    assert json.loads(resp.body.decode())['users'][0]['username'] == 'a'


def test_register_already_registered_user(mocker: pytest_mock.mocker, new_user):
    mocker.patch(
        'db.user.User.user_exists',
        autospec=True,
        return_value=True,
    )
    import service.user
    resp = service.user.register(new_user)
    assert resp.status_code == HTTPStatus.CONFLICT
    assert json.loads(resp.body.decode()) == {"message": f"Username \"{new_user.username}\" is already taken"}


def test_register_new_user(mocker: pytest_mock.mocker, new_user):
    mocker.patch(
        'db.user.User.user_exists',
        autospec=True,
        return_value=False,
    )
    mocker.patch(
        'db.user.User.register_user',
        autospec=True,
        return_value=None,
    )
    mocker.patch(
        'db.user.User.get_by_username',
        autospec=True,
        return_value={
            'id': 1,
            'username': new_user.username,
            'password': '',
        },
    )
    import service.user
    resp = service.user.register(new_user)
    assert resp.status_code == HTTPStatus.OK
    resp = json.loads(resp.body.decode())

    assert 'token' in resp
    assert 'id' in resp
    assert 'username' in resp

    assert resp['username'] == new_user.username
    assert resp['id'] == 1
    from_jwt = jwt.decode(resp['token'], Config.jwt_token_secret, algorithms=["HS256"])
    assert from_jwt == {'id': 1}


def test_login_ok(mocker: pytest_mock.mocker, new_user):
    mocker.patch(
        'db.user.User.get_by_username',
        autospec=True,
        return_value={
            'id': 1,
            'username': new_user.username,
            'password': base64.b64encode(bcrypt.hashpw(new_user.password.encode(), bcrypt.gensalt())),
        },
    )
    import service.user
    resp = service.user.login(new_user)
    assert resp.status_code == HTTPStatus.OK
    resp = json.loads(resp.body.decode())

    assert 'token' in resp
    assert 'id' in resp
    assert 'username' in resp

    assert resp['username'] == new_user.username
    assert resp['id'] == 1
    from_jwt = jwt.decode(resp['token'], Config.jwt_token_secret, algorithms=["HS256"])
    assert from_jwt == {'id': 1}


def test_login_invalid_password(mocker: pytest_mock.mocker, new_user):
    mocker.patch(
        'db.user.User.get_by_username',
        autospec=True,
        return_value={
            'id': 1,
            'username': new_user.username,
            'password': base64.b64encode(bcrypt.hashpw('test_test_test'.encode(), bcrypt.gensalt())),
        },
    )
    import service.user
    resp = service.user.login(new_user)
    assert resp.status_code == HTTPStatus.NOT_FOUND
    print(resp.body.decode())
    assert resp.body.decode() == '"user or password is incorrect"'
