import uuid
from sqlalchemy import Column, String, Enum as SQLAEnum, Integer, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum

from models.base import BaseModel


class Busyness(str, Enum):
    FULL = "full"
    PARTIAL = "partial"
    PROJECT = "project"
    VOLUNTEERING = "volunteering"
    INTERNSHIP = "internship"
    GPH = "gph"


class Experience(str, Enum):
    NO = "no experience"
    JUNIOR = "junior"  # 1 - 3
    MIDDLE = "middle"  # 3 - 6
    SENIOR = "senior"  # > 6


class VacancyModel(BaseModel):
    __tablename__ = 'vacancies'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    name = Column(String(length=50), index=True, nullable=False)
    description = Column(String(length=2000), nullable=True)
    salary = Column(Integer, nullable=True)
    experience = Column(SQLAEnum(Experience), nullable=True)
    busyness = Column(ARRAY(SQLAEnum(Busyness)), nullable=True)

