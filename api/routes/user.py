from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.dtoModels.userDTO import UserDTO
from models.dbModels.User.crud import create_user, get_all_users, get_user_by_email
from models.dbModels.User.crud import UserBasicResponse, UserResponse
from models.dbModels.User.crud import get_all_users
from .auth import get_current_employer_user
from db.session import fastapi_get_db

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def create_user_endpoint(user: UserDTO, db: AsyncSession = Depends(fastapi_get_db)):
    try:
        existing_user = await get_user_by_email(db, user.email)
        if existing_user is not None:
            raise HTTPException(status_code=403, detail="User with this email already exists")

        db_user = await create_user(db, user)
        return db_user

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        print(f"Error while creating user: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/all")
async def get_users_endpoint(
    db: AsyncSession = Depends(fastapi_get_db),
    current_user: UserBasicResponse = Depends(get_current_employer_user),
):
    users = await get_all_users(db)
    return users

