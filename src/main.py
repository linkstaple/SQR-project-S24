import uvicorn
from fastapi import FastAPI
from api.setup import setup as setup_api
from static.setup import setup as setup_static

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

app = FastAPI()
setup_api(app)
setup_static(app)
