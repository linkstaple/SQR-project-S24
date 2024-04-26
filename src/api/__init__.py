from model import RegisterUser, LoginUser, CreateGroup
import service.user
import service.group
from typing import Annotated
from fastapi import Header


def setup(app):
    @app.post("/api/register")
    async def register(user: RegisterUser):
        return await service.user.register(user)

    @app.post("/api/login")
    async def login(user: LoginUser):
        return await service.user.login(user)

    @app.get("/api/profile")
    async def profile(authorization: Annotated[str | None, Header()] = None):
        return await service.user.get_self(authorization)

    @app.get("/api/groups")
    async def groups():
        # todo extract user_id from request
        return await service.group.get_users(1)

    @app.post("/api/group")
    async def group(group_data: CreateGroup):
        return {"message": "Hello World"}

    @app.get("/api/group/{id}")
    async def group_info(id: str):
        return {"message": "Hello World"}

    @app.post("/api/split")
    async def group():
        return {"message": "Hello World"}
