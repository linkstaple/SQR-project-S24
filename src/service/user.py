from http import HTTPStatus

from db.user import User as UserDB
import model
from fastapi.responses import JSONResponse
import jwt
from config import Config
from service.passwords import hash_password, check_password


async def register(user: model.RegisterUser):
    username, password = user.username, hash_password(user.password)

    user_exists = UserDB.user_exists(username)
    if user_exists:
        return JSONResponse(
            content={'message': "Username \"{username}\" is already taken"},
            status_code=HTTPStatus.CONFLICT,
        )
    else:
        UserDB.register_user(username, password)
        new_user = UserDB.get_by_username(username)
        new_user['token'] = jwt.encode({"id": new_user['id']}, Config.jwt_token_secret, algorithm="HS256")
        return JSONResponse(status_code=HTTPStatus.OK, content=model.User.model_validate(new_user).model_dump())


async def login(user: model.LoginUser):
    found_user = UserDB.get_by_username(user.username)
    if found_user is None or not check_password(
            user.password,
            found_user['password']):
        resp = JSONResponse(content="user or password is incorrect")
        resp.status_code = HTTPStatus.NOT_FOUND
        return resp

    found_user['token'] = jwt.encode({"id": found_user['id']}, Config.jwt_token_secret, algorithm="HS256")
    return JSONResponse(status_code=HTTPStatus.OK, content=model.User.model_validate(found_user).model_dump())


def get_all():
    users_list = UserDB.list_users()
    users = list(map(lambda data: model.ListUser.model_validate(data).model_dump(), users_list))
    return JSONResponse(content={'users': users}, status_code=HTTPStatus.OK)


async def get_self(user_id):
    user = UserDB.get_by_id(user_id)
    # Technically we should always find user, do not catch user not found for the sake of simplicity
    user['token'] = jwt.encode({"id": user['id']}, Config.jwt_token_secret, algorithm="HS256")
    return JSONResponse(status_code=HTTPStatus.OK, content=model.User.model_validate(user).model_dump())
