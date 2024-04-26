from db.user import User as UserDB
import model
from fastapi.responses import JSONResponse
import jwt
from config import Config


async def register(user: model.RegisterUser):
    username, password = user.username, user.password

    existing_user = UserDB.get_by_credentials(username, password)
    if existing_user is not None:
        return JSONResponse(
            content={'message': "Username \"{username}\" is already taken"},
            status_code=409,
        )
    else:
        UserDB.register_user(username, password)
        new_user = UserDB.get_by_credentials(username, password)
        new_user['token'] = jwt.encode({"id": new_user['id']}, Config.jwt_token_secret, algorithm="HS256")
        return JSONResponse(status_code=200, content=model.User.model_validate(new_user).model_dump())


async def login(user: model.LoginUser):
    user = UserDB.get_by_credentials(user.username, user.password)
    if user is None:
        resp = JSONResponse(content="user or password is incorrect")
        resp.status_code = 404
        return resp

    user['token'] = jwt.encode({"id": user['id']}, Config.jwt_token_secret, algorithm="HS256")
    return JSONResponse(status_code=200, content=model.User.model_validate(user).model_dump())


async def get_self(token: str):
    try:
        payload = jwt.decode(token.split()[1], Config.jwt_token_secret, algorithms=["HS256"])
    except:
        resp = JSONResponse(content="jwt token invalid or not provided")
        resp.status_code = 403
        return resp
    user = UserDB.get_by_id(payload['id'])
    # Technically we should always find user, do not catch user not found for the sake of simpliticy
    user['token'] = jwt.encode({"id": user['id']}, Config.jwt_token_secret, algorithm="HS256")
    return JSONResponse(status_code=200, content=model.User.model_validate(user).model_dump())
