import uuid
from sqlalchemy import Column, String, Date, Enum as SQLAEnum, JSON, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
from passlib.context import CryptContext
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import BaseModel
from models.dbModels.Vacancy.vacancy import Busyness
from models.dbModels.User.user import UserModel


class Study:
    def __init__(self, institution: str, degree: str, field_of_study: str, faculty: str, end_date: str):
        self.institution = institution
        self.degree = degree
        self.field_of_study = field_of_study
        self.end_date = end_date,
        self.faculty = faculty

    def to_dict(self):
        """ Метод для преобразования объекта Study в словарь """
        return {
            "institution": self.institution,
            "degree": self.degree,
            "field_of_study": self.field_of_study,
            "end_date": self.end_date,
            "faculty": self.faculty
        }


class Courses:
    def __init__(self, name: str, organization: str, specialization: str, ear_of_study: str):
        self.name = name
        self.organization = organization
        self.specialization = specialization
        self.ear_of_study = ear_of_study,

    def to_dict(self):
        """ Метод для преобразования объекта Study в словарь """
        return {
            "name": self.name,
            "organization": self.organization,
            "specialization": self.specialization,
            "ear_of_study": self.ear_of_study,
        }


class Work:
    def __init__(self, start_time: str, end_time: str, organization: str, post: str, duties: str, sphere: str):
        self.start_time = start_time
        self.end_time = end_time
        self.organization = organization
        self.post = post,
        self.duties = duties,
        self.sphere = sphere,

    def to_dict(self):
        """ Метод для преобразования объекта Study в словарь """
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "organization": self.organization,
            "post": self.post,
            "duties": self.duties,
            "sphere": self.sphere,
        }


class ResumeModel(BaseModel):
    __tablename__ = 'resumes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    name = Column(String(length=50), index=True, nullable=False)
    study = Column(JSON, nullable=True)  # Используем JSON для хранения данных об учебе
    desired_busyness = Column(ARRAY(SQLAEnum(Busyness)), nullable=True)
    specialization = Column(ARRAY(String(length=50)), nullable=True)
    skills = Column(ARRAY(String(length=20)), nullable=True)
    about_me = Column(String(length=1000), nullable=True)
    courses = Column(JSON, nullable=True)
    work_experience = Column(ARRAY(JSON), nullable=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel", back_populates="resumes")

    def add_study(self, study: Study):
        """ Метод для добавления учебной информации """
        if not hasattr(self, 'study'):
            self.study = []
        self.study.append(study.to_dict())

    def add_courses(self, courses: Courses):
        """ Метод для добавления учебной информации """
        if not hasattr(self, 'courses'):
            self.courses = []
        self.courses.append(courses.to_dict())

    def add_work_experience(self, work: Work):
        """ Метод для добавления опыта работы """
        if not hasattr(self, 'work_experience'):
            self.work_experience = []
        self.work_experience.append(work.to_dict())

