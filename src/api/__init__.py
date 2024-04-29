import model
import service.user
import service.group
from fastapi import FastAPI
from starlette_context import context


def setup(app: FastAPI) -> None:
    @app.post("/api/register", summary="Register new user", responses={
        200: {'model': model.User},
        409: {'model': model.ErrorResponse,
              'description': 'Username is already taken'}
    })
    async def register(user: model.RegisterUser):
        return await service.user.register(user)

    @app.post("/api/login", summary="Login user", responses={
        200: {'model': model.User},
        404: {'model': model.ErrorResponse,
              'description': 'Username or password is incorrect'}
    })
    async def login(user: model.LoginUser):
        return await service.user.login(user)

    @app.get("/api/users", summary="Get all users", responses={
        200: {'model': model.UsersList},
        403: {'model': model.ErrorResponse,
              'description': 'Unauthorized request'
              }
    })
    async def list_users():
        return await service.user.get_all()

    @app.get("/api/profile", summary="Get user's profile data", responses={
        200: {'model': model.User},
        403: {'model': model.ErrorResponse,
              'description': 'Unauthorized request'
              }
    })
    async def profile():
        return await service.user.get_self(context.user_id)

    @app.get("/api/groups", summary="List groups which user belongs to",
             responses={
                 200: {'model': model.GroupList},
                 403: {'model': model.ErrorResponse,
                       'description': 'Unauthorized request'
                       }
             }
             )
    async def groups():
        return await service.group.list_users(context.user_id)

    @app.post("/api/group", summary="Create new group", responses={
        200: {'model': model.Group},
        403: {'model': model.ErrorResponse,
              'description': 'Unauthorized request'
              }
    })
    async def group(group_data: model.CreateGroup):
        return await service.group.create(context.user_id, group_data)

    @app.get("/api/group/{id}", summary="Get data of particular group",
             responses={
                 200: {'model': model.Group},
                 403: {'model': model.ErrorResponse,
                       'description': 'Unauthorized request'
                       },
                 404: {'model': model.ErrorResponse,
                       'description': '''Group is not found
                       / user is not a member of the group'''},
             }
             )
    async def group_info(id: int):
        return await service.group.get(context.user_id, id)

    @app.post("/api/split", summary="Create new expense splitting", responses={
        200: {'model': model.Group},
        403: {'model': model.ErrorResponse,
              'description': 'Unauthorized request'
              },
        404: {'model': model.ErrorResponse}}
    )
    async def split(split_data: model.Split):
        return await service.group.split(context.user_id, split_data)
