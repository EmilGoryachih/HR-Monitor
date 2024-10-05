import uuid

from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.orm import joinedload
from starlette import status

from .vacancy import VacancyModel
from ..User.crud import UserBasicResponse
from models.dbModels.Vacancy_user.vacancy_user_relation import vacancy_user_association
from ...dtoModels.vacancyDTO import VacancyDTO


class VacancyResponse(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        orm_mode = True


async def create_vacancy(db: AsyncSession, vacancy: VacancyDTO):
    db_vacancy = VacancyModel(
        name=vacancy.name,
        salary=vacancy.salary,
        description=vacancy.description,
        busyness=vacancy.busyness,
        experience=vacancy.experience,
    )
    db.add(db_vacancy)
    await db.commit()
    await db.refresh(db_vacancy)

    return VacancyResponse(id=db_vacancy.id, name=db_vacancy.name)


async def respond_to_vacancy(db: AsyncSession, vacancy_id: uuid.UUID, user_id: uuid.UUID, resume_id: uuid.UUID):
    statement = select(VacancyModel).where(VacancyModel.id == vacancy_id)
    result = await db.execute(statement)
    vacancy = result.scalar_one_or_none()

    if vacancy:
        stmt = insert(vacancy_user_association).values(user_id=user_id, vacancy_id=vacancy_id, resume_id=resume_id)
        await db.execute(stmt)
        await db.commit()
        return True

    return False


async def get_responded_users(db: AsyncSession, vacancy_id: uuid.UUID) -> list[UserBasicResponse]:
    statement = select(VacancyModel).where(VacancyModel.id == vacancy_id).options(
        joinedload(VacancyModel.responded_users)  # Загрузка связанных пользователей
    )
    result = await db.execute(statement)
    vacancy = result.scalars().first()  # Изменение здесь

    if vacancy:
        users = vacancy.responded_users
        return [UserBasicResponse(id=user.id, name=user.name, surname=user.surname, phone=user.phone, email=user.email, role=user.role)
                for user in users]

    return []


async def get_vacancy_by_id(db: AsyncSession, vacancy_id: uuid.UUID) -> VacancyResponse:
    statement = select(VacancyModel).where(VacancyModel.id == vacancy_id)
    result = await db.execute(statement)
    vacancy = result.scalar_one_or_none()

    if vacancy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")

    return vacancy


async def update_vacancy(db: AsyncSession, vacancy_id: uuid.UUID, vacancy_data: VacancyDTO, user_id: uuid.UUID):
    statement = select(VacancyModel).where(VacancyModel.id == vacancy_id)
    result = await db.execute(statement)
    vacancy = result.scalar_one_or_none()

    if vacancy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")


    vacancy.name = vacancy_data.name
    vacancy.salary = vacancy_data.salary
    vacancy.description = vacancy_data.description
    vacancy.busyness = vacancy_data.busyness
    vacancy.experience = vacancy_data.experience

    await db.commit()
    await db.refresh(vacancy)

    return VacancyResponse(id=vacancy.id, name=vacancy.name)


async def delete_vacancy(db: AsyncSession, vacancy_id: uuid.UUID, user_id: uuid.UUID):
    statement = select(VacancyModel).where(VacancyModel.id == vacancy_id)
    result = await db.execute(statement)
    vacancy = result.scalar_one_or_none()

    if vacancy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")

    await db.delete(vacancy)
    await db.commit()

    return {"detail": "Vacancy deleted successfully"}


