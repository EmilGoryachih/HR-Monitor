import uuid

from models.base import BaseModel

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import String


class UserModel(BaseModel):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    name = Column(String(length=50), index=True, nullable=False)
    surname = Column(String(length=50), index=True, nullable=True)
    phone = Column(String(length=15), index=True, nullable=True)
    email = Column(String(length=50), index=True, nullable=True)
    birth_date = Column(Date, index=True, nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r})"
