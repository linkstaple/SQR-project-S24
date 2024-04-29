import uvicorn
import middleware
import api
import static
import schema
from config import Config
from fastapi import FastAPI

if __name__ == "__main__":
    uvicorn.run("main:app", host=Config.bind_host,
                port=int(Config.bind_port), reload=Config.reload_app)

app = FastAPI()
middleware.setup(app)
api.setup(app)
static.setup(app)
schema.setup(app)
