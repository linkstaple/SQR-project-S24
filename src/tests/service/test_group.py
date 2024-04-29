import json
import sys
from http import HTTPStatus
from time import time

import pytest
import pytest_mock

sys.path.append('src/')

from config import Config

from model import RegisterUser, CreateGroup, User, Split

pytest_plugins = ('pytest_asyncio',)


@pytest.fixture
def user() -> User:
    """ returns new user without token """
    return User(
        id=1,
        username="username",
        token=''
    )


@pytest.fixture
def new_group() -> CreateGroup:
    """ returns new user without token """
    return CreateGroup(
        name="group_name",
        member_ids=['1', '2', '3'],
    )


@pytest.mark.asyncio
async def test_create_ok(mocker: pytest_mock.mocker, user, new_group):
    users_exists = mocker.patch(
        'db.user.User.users_exist',
        autospec=True,
        return_value=True,
    )
    create = mocker.patch(
        'db.group.Group.create',
        autospec=True,
        return_value=10012,
    )
    group_get = mocker.patch(
        'db.group.Group.get',
        autospec=True,
        return_value={
            'id': 10012,
            'name': new_group.name,
        },
    )
    group_get_members = mocker.patch(
        'db.group.Group.get_members',
        autospec=True,
        return_value=[
            {
                'id': 1,
                'username': f'member_name_1',
                'balance': 1.,
            },
            {
                'id': 2,
                'username': f'member_name_2',
                'balance': 2.,
            }
        ]
    )
    now = time()
    split_history_list = mocker.patch(
        'db.split_history.SplitHistory.list',
        autospec=True,
        return_value=[
            {
                "timestamp": now,
                "amount": 1.,
                "doer_id": 1.,
                "lander_id": 2,
                "payer_ids": [1, 2, 3],
            },
            {
                "timestamp": now,
                "amount": 2.,
                "doer_id": 1.,
                "lander_id": 2,
                "payer_ids": [1, 2, 3],
            },
        ],
    )
    import service.group
    resp = await service.group.create(user.id, new_group)
    assert resp.status_code == 200

    users_exists.assert_called_with(new_group.member_ids)
    create.assert_called_with(new_group.name, new_group.member_ids)
    group_get.assert_called_with(10012)
    group_get_members.assert_called_with(10012)
    split_history_list.assert_called_with(10012)

    resp = json.loads(resp.body.decode())
    assert 'id' in resp
    assert 'name' in resp
    assert 'members' in resp
    assert 'history' in resp

    assert resp['id'] == 10012
    assert resp['name'] == 'group_name'
    assert resp['members'] == [
        {
            'id': 1,
            'username': f'member_name_1',
            'balance': 1.,
        },
        {
            'id': 2,
            'username': f'member_name_2',
            'balance': 2.,
        }]
    assert resp['history'] == [{
        "timestamp": now,
        "amount": 1.,
        "doer_id": 1.,
        "lander_id": 2,
        "payer_ids": [1, 2, 3],
    },
        {
            "timestamp": now,
            "amount": 2.,
            "doer_id": 1.,
            "lander_id": 2,
            "payer_ids": [1, 2, 3],
        }, ]


@pytest.mark.asyncio
async def test_create_user_not_added(mocker: pytest_mock.mocker):
    users_exists = mocker.patch(
        'db.user.User.users_exist',
        autospec=True,
        return_value=True,
    )
    create = mocker.patch(
        'db.group.Group.create',
        autospec=True,
        return_value=10012,
    )
    group_get = mocker.patch(
        'db.group.Group.get',
        autospec=True,
        return_value={
            'id': 10012,
            'name': "group_name",
        },
    )
    group_get_members = mocker.patch(
        'db.group.Group.get_members',
        autospec=True,
        return_value=[
            {
                'id': 1,
                'username': f'member_name_1',
                'balance': 1.,
            },
            {
                'id': 2,
                'username': f'member_name_2',
                'balance': 2.,
            }
        ]
    )
    now = time()
    split_history_list = mocker.patch(
        'db.split_history.SplitHistory.list',
        autospec=True,
        return_value=[
            {
                "timestamp": now,
                "amount": 1.,
                "doer_id": 1.,
                "lander_id": 2,
                "payer_ids": [1, 2, 3],
            },
            {
                "timestamp": now,
                "amount": 2.,
                "doer_id": 1.,
                "lander_id": 2,
                "payer_ids": [1, 2, 3],
            },
        ],
    )
    import service.group
    resp = await service.group.create(1, CreateGroup(
        name='группа',
        member_ids=[2, 3]
    ))
    assert resp.status_code == 200

    users_exists.assert_called_with([2, 3])
    create.assert_called_with('группа', [2, 3, 1])
    group_get.assert_called_with(10012)
    group_get_members.assert_called_with(10012)
    split_history_list.assert_called_with(10012)

    resp = json.loads(resp.body.decode())
    assert 'id' in resp
    assert 'name' in resp
    assert 'members' in resp
    assert 'history' in resp

    assert resp['id'] == 10012
    assert resp['name'] == 'group_name'
    assert resp['members'] == [
        {
            'id': 1,
            'username': f'member_name_1',
            'balance': 1.,
        },
        {
            'id': 2,
            'username': f'member_name_2',
            'balance': 2.,
        },
    ]
    assert resp['history'] == [
        {
            "timestamp": now,
            "amount": 1.,
            "doer_id": 1.,
            "lander_id": 2,
            "payer_ids": [1, 2, 3],
        },
        {
            "timestamp": now,
            "amount": 2.,
            "doer_id": 1.,
            "lander_id": 2,
            "payer_ids": [1, 2, 3],
        },
    ]


@pytest.mark.asyncio
async def test_create_validation_error(mocker: pytest_mock.mocker):
    import service.group
    resp = await service.group.create(1, CreateGroup(
        name='группа',
        member_ids=[1, 1, 2]
    ))
    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert resp.body.decode() == '"invalid list of members (empty, contains only you, or contains duplicates)"'


@pytest.mark.asyncio
async def test_split_ok(mocker: pytest_mock.mocker):
    group_get = mocker.patch(
        'db.group.Group.get',
        autospec=True,
        return_value={
            'id': 10012,
            'name': 'группа',
        },
    )

    group_get_members = mocker.patch(
        'db.group.Group.get_members',
        autospec=True,
        return_value=[
            {
                'id': 1,
                'username': f'member_name_1',
                'balance': 1.,
            },
            {
                'id': 2,
                'username': f'member_name_2',
                'balance': 2.,
            },
            {
                'id': 3,
                'username': f'member_name_3',
                'balance': 3.,
            }
        ]
    )

    now = time()
    split_history_list = mocker.patch(
        'db.split_history.SplitHistory.list',
        autospec=True,
        return_value=[
            {
                "timestamp": now,
                "amount": 1.,
                "doer_id": 1.,
                "lander_id": 2,
                "payer_ids": [1, 2, 3],
            },
            {
                "timestamp": now,
                "amount": 2.,
                "doer_id": 1.,
                "lander_id": 2,
                "payer_ids": [1, 2, 3],
            },
        ],
    )

    split_history_add_tx = mocker.patch(
        'db.group.Group.add_transaction',
        autospec=True,
        return_value=[
        ],
    )

    import service.group
    resp = await service.group.split(1, Split(
        group_id=10012,
        amount=100,
        lander_id=1,
        payer_ids=[1, 2, 3]
    ))

    group_get.assert_called_with(10012)
    group_get_members.assert_called_with(10012)
    split_history_list.assert_called_with(10012)
    split_history_add_tx.assert_called_with(10012, 1, 1, [1, 2, 3], 100)

    assert resp.status_code == 200
    resp = json.loads(resp.body.decode())
    assert 'id' in resp
    assert 'name' in resp
    assert 'members' in resp
    assert 'history' in resp

    assert resp['id'] == 10012
    assert resp['name'] == 'группа'
    assert resp['members'] == [
        {
            'id': 1,
            'username': f'member_name_1',
            'balance': 1.,
        },
        {
            'id': 2,
            'username': f'member_name_2',
            'balance': 2.,
        },
        {
            'id': 3,
            'username': f'member_name_3',
            'balance': 3.,
        }
    ]
    assert resp['history'] == [
        {
            "timestamp": now,
            "amount": 1.,
            "doer_id": 1.,
            "lander_id": 2,
            "payer_ids": [1, 2, 3],
        },
        {
            "timestamp": now,
            "amount": 2.,
            "doer_id": 1.,
            "lander_id": 2,
            "payer_ids": [1, 2, 3],
        },
    ]
