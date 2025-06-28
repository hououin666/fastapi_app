import asyncio

from fastapi import APIRouter
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core import db_helper
from core.models import User, Profile, Post


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


async def demo_m2m(session: AsyncSession):
    pass


async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session)
        await demo_m2m(session)






if __name__ == '__main__':
    asyncio.run(main())