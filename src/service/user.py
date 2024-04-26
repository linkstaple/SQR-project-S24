from db.user import User as UserDB
from model import RegisterUser, LoginUser
from fastapi.responses import JSONResponse


async def register(user: RegisterUser):
    username, password = user.username, user.password

    existing_user = UserDB.get_user_by_credentials(username, password)
    if existing_user is not None:
        return JSONResponse(
            content={'message': "Username \"{username}\" is already taken"},
            status_code=409,
        )
    else:
        UserDB.register_user(username, password)
        new_user = UserDB.get_user_by_credentials(username, password)
        return JSONResponse(status_code=200, content=new_user.model_dump())


async def login(user: LoginUser):
    user = UserDB.get_user_by_credentials(user.username, user.password)
    if user is None:
        resp = JSONResponse(content="user or password is incorrect")
        resp.status_code = 404
        return resp
    resp = JSONResponse(content=user.model_dump())
    return resp
