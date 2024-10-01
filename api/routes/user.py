from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from ...models.dtoModels.userDTO import User
from ...models.dbModels.User.crud import create_user, get_all_users
from db.session import fastapi_get_db
from ...models.dbModels.User.crud import UserBasicResponse

router = APIRouter()


@router.post("/", response_model=UserBasicResponse)
async def create_user_endpoint(user: User, db: AsyncSession = Depends(fastapi_get_db)):
    db_user = await create_user(db, user)
    return db_user


@router.get("/all")
async def get_users_endpoint(db: AsyncSession = Depends(fastapi_get_db)):
    users = await get_all_users(db)
    return users

