import uvicorn
import middleware
import api
import static
from config import Config
from fastapi import FastAPI

if __name__ == "__main__":
    uvicorn.run("main:app", host=Config.bind_host, port=Config.bind_port, reload=True)

app = FastAPI()
middleware.setup(app)
api.setup(app)
static.setup(app)
