"""
Create
Read
Update
Delete
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Item
from .schemas import ItemCreate, ItemUpdate, ItemUpdatePartial


async def get_items(session: AsyncSession) -> list[Item]:
    stmt = select(Item).order_by(Item.id)
    result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_item(session: AsyncSession, product_id: int) -> Item | None:
    return await session.get(Item, product_id)


async def create_item(session: AsyncSession, item_in: ItemCreate ) -> Item:
    item = Item(**item_in.model_dump())
    session.add(item)
    await session.commit()
    # await session.refresh(item)
    return item


async def update_item(session: AsyncSession, item: Item ,item_update: ItemUpdate | ItemUpdatePartial, partial: bool = False) -> Item:
    for name, value in item_update.model_dump(exclude_unset=partial).items():
        setattr(item,name,value)
    await session.commit()
    return item


async  def delete_item(session: AsyncSession, item: Item) -> None:
    await session.delete(item)
    await session.commit()



