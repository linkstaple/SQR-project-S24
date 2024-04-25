import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db.sqlite import Database

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static")

# Dependency
def get_db():
    if not hasattr(get_db, "db"):
        get_db.db = Database()

    return get_db.db


@app.get("/api/")
async def root(db: Database = Depends(get_db)):
    return {"message": db.list_users()}


@app.post("/api/register")
async def register():
    return {"message": "Hello World"}


@app.post("/api/login")
async def login():
    return {"message": "Hello World"}


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

@app.get("/easter_egg", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )
