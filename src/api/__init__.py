import model
import service.user
import service.group
from fastapi import FastAPI, Request


def setup(app: FastAPI) -> None:
    @app.post("/api/register")
    async def register(user: model.RegisterUser):
        return await service.user.register(user)

    @app.post("/api/login")
    async def login(user: model.LoginUser):
        return await service.user.login(user)

    @app.get("/api/users")
    async def list_users():
        return await service.user.get_all()

    @app.get("/api/profile")
    async def profile(request: Request):
        return await service.user.get_self(request.state.user_id)

    @app.get("/api/groups")
    async def groups(request: Request):
        return await service.group.list_users(request.state.user_id)

    @app.post("/api/group")
    async def group(group_data: model.CreateGroup, request: Request):
        return await service.group.create(request.state.user_id, group_data)

    @app.get("/api/group/{id}")
    async def group_info(id: int, request: Request):
        return await service.group.get(request.state.user_id, id)

    @app.post("/api/split")
    async def split(split_data: model.Split, request: Request):
        return await service.group.split(request.state.user_id, split_data)
