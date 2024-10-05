from enum import Enum
from sqlalchemy import Column, Table, ForeignKey, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID
from models.base import BaseModel

class Status(str, Enum):
    INVITATIONTOINTERVIEW = "invitation to interview"
    INTERVIEWED = "interviewed"
    INVITATIONTOTEST = "invitation to test"
    TESTED = "tested"
    PROBATIONPERIOD = "probation period"

vacancy_user_association = Table(
    'vacancy_user_association',
    BaseModel.metadata,
    Column('vacancy_id', UUID(as_uuid=True), ForeignKey('vacancies.id'), primary_key=True),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('status', SQLAEnum(Status), nullable=True),  # Название для колонки "status"
)
