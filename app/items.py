# from typing import List
#
# from pydantic import BaseModel
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import DeclarativeBase
# from fastapi import APIRouter
#
# router = APIRouter(prefix='/items')
#
# class ItemModel(BaseModel):
#     name: str
#     description: str
#
# items = []
#
# @router.get('')
# async def get_items():
#     if items:
#         return items
#     else:
#         return {'message': 'No items'}
#
# @router.post('')
# async def create_item(item: ItemModel, session: AsyncSession ):
#     new_item = ItemModel(
#         name = item.name,
#         description = item.description
#     )
#     session.add(new_item)
#     await session.flush()
#     items.append(new_item)
#     return new_item