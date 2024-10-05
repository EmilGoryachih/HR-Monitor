import uuid

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from models.dbModels.Vacancy.vacancy import VacancyModel
from models.dbModels.User.user import UserModel
from .vacancy_user_relation import vacancy_user_association, Status
from models.dtoModels.vacancyDTO import VacancyDTO
from fastapi import HTTPException


async def update_vacancy_user_status(db: AsyncSession, vacancy_id: uuid.UUID, user_id: uuid.UUID, status: Status):
    # Найдем запись в таблице связи вакансий и пользователей
    stmt = (
        select(vacancy_user_association)
        .where(vacancy_user_association.c.vacancy_id == vacancy_id)
        .where(vacancy_user_association.c.user_id == user_id)
    )

    result = await db.execute(stmt)
    association_row = result.fetchone()

    if not association_row:
        raise HTTPException(status_code=404, detail="User response not found for this vacancy")

    # Обновим статус
    update_stmt = (
        update(vacancy_user_association)
        .where(vacancy_user_association.c.vacancy_id == vacancy_id)
        .where(vacancy_user_association.c.user_id == user_id)
        .values(status=status)
    )
    await db.execute(update_stmt)
    await db.commit()

    return {"detail": "Status updated successfully"}
