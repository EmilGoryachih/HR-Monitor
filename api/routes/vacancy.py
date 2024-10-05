from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.dtoModels.vacancyDTO import VacancyDTO
from models.dbModels.Vacancy.crud import create_vacancy, respond_to_vacancy
from models.dbModels.Vacancy.crud import VacancyResponse
from models.dbModels.User.crud import UserBasicResponse
from .auth import get_current_employer_user, get_current_user
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


@router.post("/respond/{vacancy_id}")
async def respond_to_vacancy_endpoint(vacancy_id: UUID, db: AsyncSession = Depends(fastapi_get_db),
                                      current_user: UserBasicResponse = Depends(get_current_user)):
    try:
        response = await respond_to_vacancy(db, vacancy_id, current_user.id)
        if response:
            return {"detail": "Successfully responded to the vacancy"}
        raise HTTPException(status_code=404, detail="Vacancy not found")
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(f"Error while responding to vacancy: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
