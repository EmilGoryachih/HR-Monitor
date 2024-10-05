import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from models.dbModels.Resume.resume import ResumeModel
from models.dtoModels.resumeDTO import ResumeDTO


async def create_resume(db: AsyncSession, resume_dto: ResumeDTO, user_id: uuid.UUID):
    # Преобразование study в сериализуемый формат
    study_serialized = resume_dto.study.dict() if resume_dto.study else None

    # Сериализация курсов
    courses_serialized = [course.dict() for course in resume_dto.courses]

    # Сериализация опыта работы
    work_experience_serialized = [work.dict() for work in resume_dto.work_experience]

    new_resume = ResumeModel(
        id=uuid.uuid4(),
        name=resume_dto.name,
        study=study_serialized,
        desired_busyness=resume_dto.desired_busyness,
        specialization=resume_dto.specialization,
        skills=resume_dto.skills,
        about_me=resume_dto.about_me,
        courses=courses_serialized,
        work_experience=work_experience_serialized,
        user_id=user_id
    )

    db.add(new_resume)
    await db.commit()
    await db.refresh(new_resume)

    return new_resume
