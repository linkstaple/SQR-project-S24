import json

import pytest
import pytest_mock

import sys

sys.path.append('src/')

from model import *


@pytest.fixture
def new_user() -> RegisterUser:
    """ returns new user without token """
    return RegisterUser(
        username="username",
        password="password",
    )


def test_list_users(mocker: pytest_mock.mocker, new_user):
    mocker.patch('db.user.User.list_users', autospec=True, return_value=[{'id': 1, 'username': 'a'}])
    from service.user import get_all
    resp = get_all()
    assert resp.status_code == 200
    assert json.loads(resp.body.decode())['users'][0]['id'] == 1
    assert json.loads(resp.body.decode())['users'][0]['username'] == 'a'
