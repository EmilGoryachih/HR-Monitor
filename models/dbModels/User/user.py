import uuid
from sqlalchemy import Column, String, Date, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from enum import Enum

from models.base import BaseModel
from sqlalchemy import Table, ForeignKey, Integer


# Enum for user roles
class RoleEnum(str, Enum):
    EMPLOYER = "employer"
    EMPLOYEE = "employee"


# Table for many-to-many relationship between users and permissions
user_permissions = Table(
    'user_permissions', BaseModel.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)


class PermissionModel(BaseModel):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class UserModel(BaseModel):
    __tablename__ = 'users'

    # Existing fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    name = Column(String(length=50), index=True, nullable=False)
    surname = Column(String(length=50), index=True, nullable=True)
    phone = Column(String(length=15), index=True, nullable=True)
    email = Column(String(length=50), index=True, nullable=True)
    birth_date = Column(Date, index=True, nullable=True)

    # New role field
    role = Column(SQLAEnum(RoleEnum), default=RoleEnum.EMPLOYEE, nullable=False)

    # Relationships
    permissions = relationship("PermissionModel", secondary=user_permissions, back_populates="users")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, role={self.role!r})"


PermissionModel.users = relationship("UserModel", secondary=user_permissions, back_populates="permissions")
