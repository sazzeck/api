from typing import TYPE_CHECKING

from sqlalchemy.future import select

from .schemas import UserScheme, BaseUserScheme
from .models import UserModel

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(
    user: UserScheme, session: "AsyncSession"
) -> UserScheme:
    query: UserModel = UserModel(**user.dict())
    session.add(query)
    await session.commit()
    await session.refresh(query)
    return UserScheme.from_orm(query)


async def get_all_users(
    session: "AsyncSession"
) -> list[UserScheme]:
    state = select(UserModel).filter()
    result = await session.execute(state)
    return result.scalars().all()


async def get_user(
    user_id: int, session: "AsyncSession"
) -> UserScheme:
    state = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(state)
    return result.scalar()


async def update_user(
    user: BaseUserScheme,
    user_data: UserModel,
    session: "AsyncSession"
) -> UserScheme:
    user.username = user_data.username
    user.firstname = user_data.firstname
    user.lastname = user_data.lastname

    await session.commit()
    await session.refresh(user)

    return UserScheme.from_orm(user)


async def delete_user(
    user: UserScheme, session: "AsyncSession"
) -> None:
    await session.delete(user)
    await session.commit()
