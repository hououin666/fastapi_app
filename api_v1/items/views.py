from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from . import crud
from .schemas import ItemCreate, Item, ItemUpdate, ItemUpdatePartial
from core import db_helper

router = APIRouter(tags=['Items'])


@router.get('/', response_model=list[Item])
async def get_items(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_items(session=session)


@router.post('/', response_model=Item, status_code=HTTP_201_CREATED)
async def create_item(item_in: ItemCreate, session: AsyncSession = Depends(db_helper.session_dependency),):
    return await crud.create_item(session=session, item_in=item_in)


@router.get('/{product_id}', response_model=Item)
async def get_item(product_id: int, session: AsyncSession = Depends(db_helper.session_dependency),):
    product = await crud.get_item(session=session,product_id=product_id )
    if product:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail = f'Item {product_id} not found!',
    )


@router.put('/{item_id}')
async def update_item(item_id: int, item_update: ItemUpdate, session: AsyncSession = Depends(db_helper.session_dependency),):
    product = await crud.get_item(session=session, product_id=item_id)
    if product:
        return await crud.update_item(session=session, item=product, item_update=item_update)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Item {item_id} not found!',
    )


@router.patch('/{item_id}')
async def update_item_partial(item_id: int, item_update: ItemUpdatePartial, session: AsyncSession = Depends(db_helper.session_dependency), partial: bool = True) -> Item:
    product = await crud.get_item(session=session, product_id=item_id)
    if product:
        return await crud.update_item(session=session, item=product, item_update=item_update, partial=partial)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Item {item_id} not found!',
    )


@router.delete('/{item_id}', status_code=HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, session: AsyncSession = Depends(db_helper.session_dependency)) -> None:
    product = await crud.get_item(session=session, product_id=item_id)
    if product:
        return await crud.delete_item(session=session, item=product)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Item {item_id} not found!',
    )

