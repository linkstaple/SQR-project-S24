import jwt
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from config import Config


def setup(app: FastAPI):
    @app.middleware("http")
    async def auth(request: Request, call_next):
        if (request.url.path[:5] != '/api/'
                or request.url.path in ['/api/login', '/api/register']):
            return await call_next(request)

        token = request.headers.get("Authorization")
        try:
            payload = jwt.decode(token.split()[1],
                                 Config.jwt_token_secret, algorithms=["HS256"])
            request.state.user_id = payload['id']
        except:
            return JSONResponse(
                content="jwt token invalid or not provided",
                status_code=403)

        return await call_next(request)
