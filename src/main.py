from contextlib import asynccontextmanager
from fastapi import FastAPI

from . import models
from . import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await models.init_db()
    yield
    await models.close_db()


app = FastAPI(lifespan=lifespan)
app.include_router(routers.router)


@app.get("/")
def root():
    return {"message": "Welcome to TAT (เที่ยวไทยคนละครึ่ง)"}
