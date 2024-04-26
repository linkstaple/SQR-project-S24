import uvicorn
import api
import static
from fastapi import FastAPI

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

app = FastAPI()
api.setup(app)
static.setup(app)
