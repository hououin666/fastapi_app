
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from api_v1.users.schemas import UserCreate, User, UserBase
from core import db_helper
import crud

router = APIRouter(prefix='/users', tags=['Users'])


async def create_user(user: UserCreate, session: AsyncSession = Depends(db_helper.session_dependency)) -> User:
    return await crud.create_user(session, user.username)


async def get_user_by_username(user: UserBase, session: AsyncSession = Depends(db_helper.session_dependency)) -> User:
    user = await crud.get_user_by_username(session, user.username)
    if user:
        return user
    raise HTTPException(status_code=HTTP_204_NO_CONTENT, detail=f'User {user.username} not found!')


async def create_user_profile(user: UserBase,):
    pass
