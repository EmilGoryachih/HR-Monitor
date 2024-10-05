import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

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


async def get_all_resumes(db: AsyncSession, user_id: uuid.UUID):
    statement = select(ResumeModel).where(ResumeModel.user_id == user_id)
    result = await db.execute(statement)
    resumes = result.scalars().all()

    return resumes


async def get_resume_by_id(db: AsyncSession, user_id: uuid.UUID, resume_id: uuid.UUID):
    statement = select(ResumeModel).where(ResumeModel.id == resume_id, ResumeModel.user_id == user_id)
    result = await db.execute(statement)
    resume = result.scalar_one_or_none()

    if resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found or not authorized to view")

    return resume


async def change_resume(db: AsyncSession, resume_dto: ResumeDTO, user_id: uuid.UUID, resume_id: uuid.UUID):
    statement = select(ResumeModel).where(ResumeModel.id == resume_id, ResumeModel.user_id == user_id)
    result = await db.execute(statement)
    resume = result.scalar_one_or_none()

    if resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found or not authorized to update")

    resume.name = resume_dto.name
    resume.study = resume_dto.study.dict() if resume_dto.study else None
    resume.desired_busyness = resume_dto.desired_busyness
    resume.specialization = resume_dto.specialization
    resume.skills = resume_dto.skills
    resume.about_me = resume_dto.about_me
    resume.courses = [course.dict() for course in resume_dto.courses] if resume_dto.courses else None
    resume.work_experience = [work.dict() for work in resume_dto.work_experience] if resume_dto.work_experience else None

    await db.commit()
    await db.refresh(resume)

    return resume


async def delete_resume(db: AsyncSession, user_id: uuid.UUID, resume_id: uuid.UUID):
    statement = select(ResumeModel).where(ResumeModel.id == resume_id, ResumeModel.user_id == user_id)
    result = await db.execute(statement)
    resume = result.scalar_one_or_none()

    if resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Resume not found or not authorized to delete")

    await db.delete(resume)
    await db.commit()

    return {"detail": "Resume deleted successfully"}