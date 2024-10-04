from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.dtoModels.vacancyDTO import VacancyDTO
from models.dbModels.Vacancy.crud import create_vacancy
from models.dbModels.Vacancy.crud import VacancyResponse
from models.dbModels.User.crud import UserBasicResponse
from .auth import get_current_employer_user
from db.session import fastapi_get_db

router = APIRouter()


@router.post("/create", response_model=VacancyResponse)
async def create_vacancy_endpoint(vacancy: VacancyDTO, db: AsyncSession = Depends(fastapi_get_db),
                                  current_user: UserBasicResponse = Depends(get_current_employer_user)):
    try:
        db_user = await create_vacancy(db, vacancy)
        return db_user

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        print(f"Error while creating vacancy: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
