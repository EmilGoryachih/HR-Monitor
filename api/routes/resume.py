import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .auth import get_current_user
from db.session import fastapi_get_db
from models.dtoModels.resumeDTO import ResumeDTO
from models.dbModels.Resume.crud import create_resume

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
