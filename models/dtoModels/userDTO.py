from pydantic import BaseModel
import datetime

from models.dbModels.User.user import RoleEnum


class UserDTO(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    phone: str
    dateOfBirth: datetime.date

