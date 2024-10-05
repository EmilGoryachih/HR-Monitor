import uuid

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.orm import joinedload

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


async def respond_to_vacancy(db: AsyncSession, vacancy_id: uuid.UUID, user_id: uuid.UUID):
    # Проверим, существует ли вакансия
    statement = select(VacancyModel).where(VacancyModel.id == vacancy_id)
    result = await db.execute(statement)
    vacancy = result.scalar_one_or_none()

    if vacancy:
        # Связываем пользователя и вакансию через промежуточную таблицу
        stmt = insert(vacancy_user_association).values(user_id=user_id, vacancy_id=vacancy_id)
        await db.execute(stmt)
        await db.commit()
        return True

    return False


async def get_responded_users(db: AsyncSession, vacancy_id: uuid.UUID) -> list[UserBasicResponse]:
    # Проверим, существует ли вакансия
    statement = select(VacancyModel).where(VacancyModel.id == vacancy_id).options(
        joinedload(VacancyModel.responded_users)  # Загрузка связанных пользователей
    )
    result = await db.execute(statement)
    vacancy = result.scalars().first()  # Изменение здесь

    if vacancy:
        # Получаем всех пользователей, откликнувшихся на вакансию
        users = vacancy.responded_users
        return [UserBasicResponse(id=user.id, name=user.name, surname=user.surname, phone=user.phone, email=user.email, role=user.role)
                for user in users]

    return []


