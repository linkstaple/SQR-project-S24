from model import RegisterUser, LoginUser, CreateGroup
import service.user
import service.group
from typing import Annotated
from fastapi import Header, FastAPI
from starlette_context import context


def setup(app: FastAPI) -> None:
    @app.post("/api/register")
    async def register(user: RegisterUser):
        return await service.user.register(user)

    @app.post("/api/login")
    async def login(user: LoginUser):
        return await service.user.login(user)
    
    @app.get("/api/users")
    async def list_users():
        return await service.user.get_users()

    @app.get("/api/profile")
    async def profile():
        return await service.user.get_self(context.user_id)

    @app.get("/api/groups")
    async def groups():
        return await service.group.get_users(context.user_id)

    @app.post("/api/group")
    async def group(group_data: CreateGroup):
        return {"message": "Hello World"}

    @app.get("/api/group/{id}")
    async def group_info(id: str):
        return {"message": "Hello World"}

    @app.post("/api/split")
    async def group():
        return {"message": "Hello World"}
