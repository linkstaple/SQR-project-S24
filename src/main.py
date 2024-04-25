import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("register")
async def register():
    return {"message": "Hello World"}


@app.post("login")
async def login():
    return {"message": "Hello World"}


@app.get("profile")
async def profile():
    return {"message": "Hello World"}


@app.get("groups")
async def groups():
    return {"message": "Hello World"}


@app.post("group")
async def group():
    return {"message": "Hello World"}


@app.get("group/{id}")
async def group_info(id: str):
    return {"message": "Hello World"}


@app.post("split")
async def group():
    return {"message": "Hello World"}


if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
