from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


from models.base import BaseModel


vacancy_user_association = Table(
    'vacancy_user_association',
    BaseModel.metadata,
    Column('vacancy_id', UUID(as_uuid=True), ForeignKey('vacancies.id'), primary_key=True),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
)
