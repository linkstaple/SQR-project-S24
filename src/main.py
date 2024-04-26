import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db.sqlite import Database
from model.model import RegisterUser, LoginUser

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static-css", StaticFiles(directory="static/css"), name="static-css")
app.mount("/static-js", StaticFiles(directory="static/js"), name="static-js")

templates = Jinja2Templates(directory="static")
htmlTemplates = Jinja2Templates(directory="static/html")


# Dependency
def get_db():
    if not hasattr(get_db, "db"):
        get_db.db = Database()

    return get_db.db.new_db()


@app.get("/api/")
async def root(db: Database = Depends(get_db)):
    return {"message": db.list_users()}


@app.post("/api/register")
async def register(user: RegisterUser, db: Database = Depends(get_db)):
    username, password = user.username, user.password

    existing_user = db.get_user_by_credentials(username, password)
    if existing_user is not None:
        return JSONResponse(
            content={'message': "Username \"{username}\" is already taken"},
            status_code=409,
        )
    else:
        db.register_user(username, password)
        new_user = db.get_user_by_credentials(username, password)
        return JSONResponse(status_code=200, content=new_user.model_dump())


@app.post("/api/login")
async def login(user: LoginUser, db: Database = Depends(get_db)):
    user = db.get_user_by_credentials(user.username, user.password)
    if user is None:
        resp = JSONResponse(content="user or password is incorrect")
        resp.status_code = 404
        return resp
    resp = JSONResponse(content=user.model_dump())
    return resp


@app.get("/api/profile")
async def profile():
    return {"message": "Hello World"}


@app.get("/api/groups")
async def groups():
    return {"message": "Hello World"}


@app.post("/api/group")
async def group():
    return {"message": "Hello World"}


@app.get("/api/group/{id}")
async def group_info(id: str):
    return {"message": "Hello World"}


@app.post("/api/split")
async def group():
    return {"message": "Hello World"}

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return htmlTemplates.TemplateResponse(
        request=request, name="login.html", context={'script_type': 'login'}
    )

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return htmlTemplates.TemplateResponse(
        request=request, name="login.html", context={'script_type': 'register'}
    )

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    return htmlTemplates.TemplateResponse(
        request=request, name="profile.html"
    )

@app.get("/group/{group_id}")
def update_item(request: Request, group_id: int):
    return htmlTemplates.TemplateResponse(
        request=request, name="group.html", context={'group_id': group_id}
    )

@app.get("/easter_egg", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )
