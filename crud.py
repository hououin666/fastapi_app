import asyncio

from fastapi import APIRouter
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core import db_helper
from core.models import User, Profile, Post, Order, Item, OrderProductAssociation


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username==username)
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    print(user)
    return user


async def create_user_profile(session: AsyncSession, user_id: int, first_name: str | None, last_name: str | None) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession) -> list[User]:
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars()
    for user in users:
        print(user.profile.first_name)


async def create_posts(session: AsyncSession, user_id: int, *posts_titles: str) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(session: AsyncSession):
    stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)

    for user in users.unique():
        print('**' * 10)
        print(user)
        for post in user.posts:
            print('-', post)

async def main_relations(session: AsyncSession):
    # await create_user(session=session, username="redlikeroses")
    # await create_user(session=session, username='bob')
    user_redlikeroses = await get_user_by_username(session=session, username='redlikeroses')
    user_bob = await get_user_by_username(session=session, username='bob')
    # await create_user_profile(session=session, user_id=user_redlikeroses.id, first_name='lala', last_name='haha')
    # await create_user_profile(session=session, user_id=user_bob.id,first_name='bob', last_name='bob')\
    await show_users_with_profiles(session)
    # await create_posts(session,user_redlikeroses.id,'FastAPI intro', 'FastAPI advanced', 'FastAPI more')
    # await create_posts(session, user_bob.id, 'SQLA 2.0', 'SQLA Joins')
    await get_users_with_posts(session=session)


async def create_order(session: AsyncSession, promocode: str | None = None) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_product(session: AsyncSession, name: str, description: str, price: int) -> Item:
    product = Item(
        name=name,
        description=description,
        price=price,
    )
    session.add(product)
    await session.commit()
    return product


async def create_orders_and_products(session: AsyncSession):
    order_one = await create_order(session)
    order_promo = await create_order(session, promocode='promo')

    mouse = await create_product(session, 'Mouse', 'Great gaming mouse', 123)
    keyboard = await create_product(session, 'Keyboard', 'Great gaming keyboard', 149)
    display = await create_product(session, 'Display', 'Office display', 299)

    order_one = await session.scalar(
        select(Order).where(Order.id == order_one.id).options(selectinload(Order.products)).order_by(Order.id))
    order_promo = await session.scalar(
        select(Order).where(Order.id == order_promo.id).options(selectinload(Order.products)).order_by(Order.id))

    order_one.products.append(mouse)
    order_one.products.append(keyboard)
    order_promo.products.append(keyboard)
    order_promo.products.append(display)

    await session.commit()


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = (select(Order).options(selectinload(Order.products)).order_by(Order.id))
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_get_orders_with_products_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session)
    for order in orders:
        print(order.id, order.promocode, order.created_at, 'products:')
        for product in order.products:
            print('-', product.id, product.name, product.price)


async def get_orders_with_products_assoc(session: AsyncSession) -> list[Order]:
    stmt = (select(Order).options(selectinload(Order.products_details).joinedload(OrderProductAssociation.product)).order_by(Order.id))
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_get_orders_with_products_with_assoc(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)
    for order in orders:
        print(order.id, order.promocode, order.created_at, 'products:')
        for order_product_detail in order.products_details:
            print('-', order_product_detail.product.id, order_product_detail.product.name, order_product_detail.product.price)


async def demo_m2m(session: AsyncSession):
    # await create_orders_and_products(session)
    # await demo_get_orders_with_products_through_secondary(session)
    await demo_get_orders_with_products_with_assoc(session)



async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session)
        await demo_m2m(session)






if __name__ == '__main__':
    asyncio.run(main())