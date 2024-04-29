import dataclasses
import json
import os
import sys
import traceback
import typing
from time import sleep

from httpx import AsyncClient

import pytest
from fastapi import FastAPI

sys.path.append('src')

from model import Group, GroupList

pytest_plugins = ('pytest_asyncio',)


def set_up(mocker) -> FastAPI:
    os.open('test_lazy_split.db', flags=os.O_CREAT)

    sys.path.append('src/')

    users_exists = mocker.patch(
        'config.Config.sqlite_path',
        'test_lazy_split.db',
    )

    import api
    import middleware
    import static

    app = FastAPI()
    middleware.setup(app)
    api.setup(app)
    static.setup(app)

    return app


def teardown():
    os.remove('test_lazy_split.db')


@dataclasses.dataclass
class User:
    id: int
    username: str
    password: str
    token: str


async def register_user(app: FastAPI, base_url: str, username: str, password: str) -> User:
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.request("POST", '/api/register',
                                    json={
                                        "username": username,
                                        "password": password,
                                    })
        assert response.status_code == 200

        resp = response.json()
        user = User(
            username=username,
            password=password,
            id=resp['id'],
            token=resp['token'],
        )

        return user


async def get_profile(app: FastAPI, base_url: str, user: User) -> User:
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.request("GET", '/api/profile', headers={
            "Authorization": f"Bearer {user.token}"
        })
        assert response.status_code == 200

        print(response.json())
        return User(
            username=response.json()["username"],
            id=response.json()['id'],
            token=response.json()['token'],
            password='',
        )


async def create_group(app: FastAPI, base_url: str, user: User, group_name: str, user_ids: typing.List[int]) -> Group:
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.request("POST", '/api/group', json={
            "name": group_name,
            "member_ids": user_ids,
        }, headers={
            "Authorization": f"Bearer {user.token}",
        })
        assert response.status_code == 200

        return Group.model_validate(response.json())


async def list_groups(app: FastAPI, base_url: str, user: User) -> GroupList:
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.request("GET", '/api/groups', headers={
            "Authorization": f"Bearer {user.token}",
        })
        assert response.status_code == 200

        return GroupList.model_validate(response.json())


async def get_group_info(app: FastAPI, base_url: str, user: User, group_id: int) -> Group:
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.request("GET", f'/api/group/{group_id}', headers={
            "Authorization": f"Bearer {user.token}",
        })
        assert response.status_code == 200

        return Group.model_validate(response.json())


async def split_money(app: FastAPI, base_url: str, user: User, group_id: int, amount: float,
                      payers: typing.List[int]) -> Group:
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.request("POST", f'/api/split', json={
            "group_id": group_id,
            "amount": amount,
            "lander_id": user.id,
            "payer_ids": payers,

        }, headers={
            "Authorization": f"Bearer {user.token}",
        })
        assert response.status_code == 200

        return Group.model_validate(response.json())


@pytest.mark.asyncio
async def test_api_common_operations(mocker):
    app = set_up(mocker)

    try:
        base_url = "http://127.0.0.1:8000"
        user1 = await register_user(app, base_url,
                                    'timur', '123')
        user2 = await register_user(app, base_url,
                                    'andrey', '1234')
        user3 = await register_user(app, base_url,
                                    'misha', '12345')

        profile_user_3 = await get_profile(app, base_url, user3)
        assert profile_user_3.id == user3.id
        assert profile_user_3.username == user3.username

        group_1_2 = await create_group(app, base_url,
                                       user1, "sky part", [user2.id])

        group_1_3 = await create_group(app, base_url,
                                       user1, "restaurant", [user1.id, user3.id])

        group_all = await create_group(app, base_url,
                                       user1, "party", [user2.id, user3.id])

        user_3_groups = await list_groups(app, base_url, user3)
        assert len(user_3_groups.groups) == 2
        assert user_3_groups.groups[0].id == group_1_3.id
        assert user_3_groups.groups[1].id == group_all.id
        assert user_3_groups.groups[0].name == group_1_3.name
        assert user_3_groups.groups[1].name == group_all.name

        group_all_info = await get_group_info(app, base_url,
                                              user3, group_all.id)
        assert group_all_info == group_all

        await split_money(app, base_url, user2, group_1_2.id, 100, [user1.id])
        await split_money(app, base_url, user2, group_1_2.id, 100, [user1.id, user2.id])

        await split_money(app, base_url, user1, group_all.id, 300, [user1.id, user2.id, user3.id])
        await split_money(app, base_url, user3, group_all.id, 600, [user1.id, user2.id, user3.id])
        await split_money(app, base_url, user3, group_all.id, 300, [user1.id, user2.id, user3.id])

        group_all_info = await get_group_info(app, base_url,
                                              user3, group_all.id)
        assert len(group_all_info.history) == 3
        assert group_all_info.members[0].balance == -400.
        assert group_all_info.members[1].balance == 500.
        assert group_all_info.members[2].balance == -100.

        group_1_3_info = await get_group_info(app, base_url,
                                              user3, group_1_3.id)

        assert len(group_all_info.history) == 0
        assert group_1_3_info.members[0].balance == 0.
        assert group_1_3_info.members[1].balance == 0.

        group_1_2_info = await get_group_info(app, base_url,
                                              user1, group_1_2.id)

        assert len(group_all_info.history) == 2
        assert group_1_2_info.members[0].balance == 150.
        assert group_1_2_info.members[1].balance == -150.

    except Exception as e:
        print("exception: ", e, traceback.format_exc())

    teardown()
