from pydantic import BaseModel
import datetime


class User(BaseModel):
    name: str
    surname: str
    email: str
    phone: str
    dateOfBirth: datetime.date

