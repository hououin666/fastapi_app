from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from app.movies import router as movies_router
from api_v1 import router as router_v1
from crud import router as user_router
from core.models import Base
from core import db_helper, DatabaseHelper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix='/api/v1')
app.include_router(movies_router)
app.include_router(user_router)


@app.get('/')
async def index():
    return {'Главная': 'Страница'}








