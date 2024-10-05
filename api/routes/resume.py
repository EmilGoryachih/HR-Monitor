import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .auth import get_current_user
from db.session import fastapi_get_db
from models.dtoModels.resumeDTO import ResumeDTO
from models.dbModels.Resume.crud import create_resume, get_all_resumes, get_resume_by_id, change_resume, delete_resume

from models.dbModels.User.crud import UserBasicResponse

router = APIRouter()


@router.post("/create")
async def create_vacancy_endpoint(vacancy: ResumeDTO, db: AsyncSession = Depends(fastapi_get_db),
                                  current_user: UserBasicResponse = Depends(get_current_user)):
    try:
        db_resume = await create_resume(db, vacancy, current_user.id)
        return db_resume

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        print(f"Error while creating resume: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/all")
async def get_all_user_resumes_endpoint(db: AsyncSession = Depends(fastapi_get_db), current_user: UserBasicResponse = Depends(get_current_user)):
    try:
        resumes = await get_all_resumes(db, current_user.id)
        return resumes

    except Exception as e:
        print(f"Error while getting all resumes: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{resume_id}")
async def get_resume_endpoint(resume_id: uuid.UUID, db: AsyncSession = Depends(fastapi_get_db), current_user: UserBasicResponse = Depends(get_current_user)):
    try:
        resume = await get_resume_by_id(db, current_user.id, resume_id)
        return resume

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        print(f"Error while getting resume: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/{resume_id}")
async def update_resume_endpoint(resume_id: uuid.UUID, resume_data: ResumeDTO, db: AsyncSession = Depends(fastapi_get_db), current_user: UserBasicResponse = Depends(get_current_user)):
    try:
        updated_resume = await change_resume(db, resume_data, current_user.id, resume_id)
        return updated_resume

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        print(f"Error while updating resume: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{resume_id}")
async def delete_resume_endpoint(resume_id: uuid.UUID, db: AsyncSession = Depends(fastapi_get_db), current_user: UserBasicResponse = Depends(get_current_user)):
    try:
        result = await delete_resume(db, current_user.id, resume_id)
        return result

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        print(f"Error while deleting resume: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
