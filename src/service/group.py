from db.group import Group as GroupDB
from fastapi.responses import JSONResponse


async def get_users(user_id):
    user_groups = GroupDB.get_user_groups(user_id)
    return JSONResponse(content={'groups': list(map(lambda model: model.model_dump(), user_groups))}, status_code=200)
