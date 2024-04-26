from db.group import Group as GroupDB
from fastapi.responses import JSONResponse

from model import CreateGroup


async def create(user_id, group_data: CreateGroup) -> JSONResponse:
    id = GroupDB.create(group_data.name, group_data.member_ids + [user_id])
    return JSONResponse(status_code=200, content=id)


async def get_users(user_id):
    user_groups = GroupDB.get_user_groups(user_id)
    return JSONResponse(content={'groups': list(map(lambda model: model.model_dump(), user_groups))}, status_code=200)
