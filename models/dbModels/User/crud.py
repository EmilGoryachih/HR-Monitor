import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from .user import UserModel
from ...dtoModels.userDTO import User
from sqlalchemy.future import select


from pydantic import BaseModel


class UserBasicResponse(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        orm_mode = True


async def create_user(db: AsyncSession, user: User):
    db_user = UserModel(
        name=user.name,
        surname=user.surname,
        phone=user.phone,
        birth_date=user.dateOfBirth,
        email=user.email,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return UserBasicResponse(id=db_user.id, name=db_user.name)


async def get_all_users(db: AsyncSession):
    statement = select(UserModel)
    result = await db.execute(statement)
    users = result.scalars().all()
    return users


async def get_user_by_id(db: AsyncSession, id: uuid.UUID) -> UserBasicResponse | None:
    statement = select(UserModel).where(id == UserModel.id)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if user:
        return UserBasicResponse(id=user.id, name=user.name)

    return None
