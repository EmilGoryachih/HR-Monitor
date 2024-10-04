from fastapi import APIRouter

from .routes import user, login, vacancy

api_router = APIRouter()

api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(vacancy.router, prefix="/vacancies", tags=["vacancies"])
