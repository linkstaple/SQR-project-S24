from http import HTTPStatus

from db.group import Group as GroupDB
from fastapi.responses import JSONResponse
import model


async def create(user_id, group_data: model.CreateGroup) -> JSONResponse:
    if len(group_data.member_ids) != len(set(group_data.member_ids)) or len(group_data.member_ids) == 0:
        return JSONResponse(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            content='invalid list of members (empty or contains duplicates)')
    if user_id not in group_data.member_ids:
        group_data.member_ids.append(user_id)
    id = GroupDB.create(group_data.name, group_data.member_ids)
    group = GroupDB.get(id)
    group['members'] = GroupDB.get_members(id)
    group['history'] = GroupDB.get_history(id)
    return JSONResponse(status_code=HTTPStatus.OK, content=model.Group.model_validate(group).model_dump())


async def get(user_id, group_id) -> JSONResponse:
    group = GroupDB.get(group_id)
    if group is None:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content='group not found')
    group['members'] = GroupDB.get_members(group_id)
    if user_id not in map(lambda member: member['id'], group['members']):
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content='group not found')
    group['history'] = GroupDB.get_history(group_id)
    return JSONResponse(status_code=HTTPStatus.OK, content=model.Group.model_validate(group).model_dump())


async def list(user_id):
    groups = GroupDB.list(user_id)
    return JSONResponse(content=model.GroupList.model_validate({'groups': groups}).model_dump(),
                        status_code=HTTPStatus.OK)
