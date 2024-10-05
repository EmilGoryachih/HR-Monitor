from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from models.dbModels.Vacancy.crud import respond_to_vacancy, get_responded_users
from .auth import get_current_employer_user, get_current_user
from models.dbModels.Vacancy_user.crud import update_vacancy_user_status
from models.dbModels.Vacancy_user.vacancy_user_relation import Status
from db.session import fastapi_get_db
from models.dbModels.User.crud import UserBasicResponse

router = APIRouter()


@router.put("/vacancy/{vacancy_id}/user/{user_id}/status", status_code=200)
async def update_user_status(
        vacancy_id: UUID,
        user_id: UUID,
        status: Status,
        db: AsyncSession = Depends(fastapi_get_db),
        current_user: UserBasicResponse = Depends(get_current_employer_user)  # Проверяем права пользователя
):
    # Проверим, имеет ли текущий пользователь права employer или owner
    if current_user.role not in ["employer", "owner"]:
        raise HTTPException(status_code=403, detail="You don't have permission to update status")

    try:
        # Обновляем статус пользователя на выбранной вакансии
        response = await update_vacancy_user_status(db, vacancy_id, user_id, status)
        return response

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        print(f"Error while updating user status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/respond/{vacancy_id}/{resume_id}")
async def respond_to_vacancy_endpoint(vacancy_id: UUID, resume_id: UUID, db: AsyncSession = Depends(fastapi_get_db),
                                      current_user: UserBasicResponse = Depends(get_current_user),
                                      ):
    try:
        response = await respond_to_vacancy(db, vacancy_id, current_user.id, resume_id)
        if response:
            return {"detail": "Successfully responded to the vacancy"}
        raise HTTPException(status_code=404, detail="Vacancy not found")
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(f"Error while responding to vacancy: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/respondedUsers/{vacancy_id}", response_model=list[UserBasicResponse])
async def get_responded_users_endpoint(vacancy_id: UUID, db: AsyncSession = Depends(fastapi_get_db),
                                       current_user: UserBasicResponse = Depends(get_current_employer_user)):
    try:
        # Получаем список пользователей, откликнувшихся на вакансию
        responded_users = await get_responded_users(db, vacancy_id)

        if not responded_users:
            raise HTTPException(status_code=404, detail="No users found for this vacancy")

        return responded_users
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(f"Error while fetching responded users: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

