import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
