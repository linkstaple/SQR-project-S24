from model.model import RegisterUser, LoginUser
from service.user import register as user_register, login as user_login
from service.group import get_user_groups

def setup(app):
    @app.get("/api/")
    async def root():
        return {"message": user.list_users()}


    @app.post("/api/register")
    async def register(user: RegisterUser):
        return await user_register(user)


    @app.post("/api/login")
    async def login(user: LoginUser):
        return await user_login(user)


    @app.get("/api/profile")
    async def profile():
        return {"message": "Hello World"}


    @app.get("/api/groups")
    async def groups():
        return await get_user_groups(1) #todo extract user_id from request


    @app.post("/api/group")
    async def group():
        return {"message": "Hello World"}


    @app.get("/api/group/{id}")
    async def group_info(id: str):
        return {"message": "Hello World"}


    @app.post("/api/split")
    async def group():
        return {"message": "Hello World"}

