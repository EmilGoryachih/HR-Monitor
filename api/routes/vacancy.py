from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.dtoModels.vacancyDTO import VacancyDTO
from models.dbModels.Vacancy.crud import create_vacancy, get_vacancy_by_id, delete_vacancy, update_vacancy
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


@router.get("/{vacancy_id}", response_model=VacancyDTO)
async def get_vacancy_endpoint(vacancy_id: UUID, db: AsyncSession = Depends(fastapi_get_db),
                               current_user: UserBasicResponse = Depends(get_current_user)):
    try:
        vacancy = await get_vacancy_by_id(db, vacancy_id)
        return vacancy

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        print(f"Error while getting vacancy: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/{vacancy_id}", response_model=VacancyResponse)
async def update_vacancy_endpoint(vacancy_id: UUID, vacancy_data: VacancyDTO,
                                  db: AsyncSession = Depends(fastapi_get_db),
                                  current_user: UserBasicResponse = Depends(get_current_employer_user)):
    try:
        updated_vacancy = await update_vacancy(db, vacancy_id, vacancy_data, current_user.id)
        return updated_vacancy

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        print(f"Error while updating vacancy: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{vacancy_id}")
async def delete_vacancy_endpoint(vacancy_id: UUID, db: AsyncSession = Depends(fastapi_get_db),
                                  current_user: UserBasicResponse = Depends(get_current_employer_user)):
    try:
        result = await delete_vacancy(db, vacancy_id, current_user.id)
        return result

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        print(f"Error while deleting vacancy: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
