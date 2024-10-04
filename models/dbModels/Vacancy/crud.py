import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from .vacancy import VacancyModel
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


