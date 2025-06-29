from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.movies import router as movies_router
from api_v1 import router as router_v1
# from crud import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix='/api/v1')
app.include_router(movies_router)
# app.include_router(user_router)


@app.get('/')
async def index():
    return {'Главная': 'Страница'}








