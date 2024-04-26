from model import RegisterUser, LoginUser, CreateGroup
import service.user
import service.group

def setup(app):
    @app.post("/api/register")
    async def register(user: RegisterUser):
        return await service.user.register(user)


    @app.post("/api/login")
    async def login(user: LoginUser):
        return await service.user.login(user)


    @app.get("/api/profile")
    async def profile():
        return {"message": "Hello World"}


    @app.get("/api/groups")
    async def groups():
        return await service.group.get_users(1) #todo extract user_id from request


    @app.post("/api/group")
    async def group(group_data: CreateGroup):
        return {"message": "Hello World"}


    @app.get("/api/group/{id}")
    async def group_info(id: str):
        return {"message": "Hello World"}


    @app.post("/api/split")
    async def group():
        return {"message": "Hello World"}

