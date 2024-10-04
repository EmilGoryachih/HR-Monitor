import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from .user import UserModel, RoleEnum
from ...dtoModels.userDTO import User
from sqlalchemy.future import select


from pydantic import BaseModel


class UserBasicResponse(BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    phone: str
    email: str
    role: RoleEnum


class UserResponse(BaseModel):
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
        role=user.role,  # Роль передаётся из объекта User
    )
    db_user.set_password(user.password)  # Хеширование пароля
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return UserResponse(id=db_user.id, name=db_user.name)


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


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(UserModel).where(UserModel.email == email)
    )
    user = result.scalar_one_or_none()
    if user:
        return user  # Возвращаем объект UserModel с полными данными
    return None


