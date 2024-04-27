from http import HTTPStatus

from db.group import Group as GroupDB
from db.user import User as UserDB
from db.split_history import SplitHistory as SplitHistoryDB
from fastapi.responses import JSONResponse
import model


def create(user_id, group_data: model.CreateGroup) -> JSONResponse:
    if (len(group_data.member_ids) != len(set(group_data.member_ids))
            or len(group_data.member_ids) == 0
            or (len(group_data.member_ids) == 1
                and group_data.member_ids[0] == user_id)):
        return JSONResponse(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content='invalid list of members '
                    '(empty, contains only you, or contains duplicates)')

    if not UserDB.users_exist(group_data.member_ids.copy()):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content='member not found')

    if user_id not in group_data.member_ids:
        group_data.member_ids += [user_id]

    id = GroupDB.create(group_data.name, group_data.member_ids)
    group = GroupDB.get(id)
    group['members'] = GroupDB.get_members(id)
    group['history'] = SplitHistoryDB.list(id)
    return JSONResponse(status_code=HTTPStatus.OK,
                        content=model.Group.model_validate(group).model_dump())


def get(user_id, group_id) -> JSONResponse:
    group = GroupDB.get(group_id)
    if group is None:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND,
                            content='group not found')
    group['members'] = GroupDB.get_members(group_id)
    if user_id not in map(lambda member: member['id'], group['members']):
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND,
                            content='group not found')
    group['history'] = SplitHistoryDB.list(group_id)
    return JSONResponse(status_code=HTTPStatus.OK,
                        content=model.Group.model_validate(group).model_dump())


async def list_users(user_id):
    groups = GroupDB.list_users(user_id)
    return JSONResponse(content=model.GroupList.model_validate(
        {'groups': groups}).model_dump(), status_code=HTTPStatus.OK)


def split(user_id, split_data: model.Split):
    if len(split_data.payer_ids) != len(
            set(split_data.payer_ids)) or len(split_data.payer_ids) == 0:
        return JSONResponse(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content='invalid list of payers (empty or contains duplicates)')
    if split_data.amount <= 0:
        return JSONResponse(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content='amount less or equal to zero')

    group = GroupDB.get(split_data.group_id)
    if group is None:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content='group not found')
    group['members'] = GroupDB.get_members(split_data.group_id)
    if user_id not in map(lambda member: member['id'], group['members']):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content='group not found')

    member_ids = list(map(lambda member: member['id'], group['members']))
    for payer_id in split_data.payer_ids:
        if payer_id not in member_ids:
            return JSONResponse(
                status_code=HTTPStatus.NOT_FOUND,
                content='payer not found within the group')
    if split_data.lander_id not in member_ids:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content='lander not found within the group')

    GroupDB.add_transaction(
        group['id'],
        user_id,
        split_data.lander_id,
        split_data.payer_ids,
        split_data.amount)
    return get(user_id, group['id'])
