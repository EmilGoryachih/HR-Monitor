from pydantic import BaseModel, constr
from typing import List, Optional


class StudyDTO(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    faculty: str
    end_date: str


class CourseDTO(BaseModel):
    name: str
    organization: str
    specialization: str
    year_of_study: str


class WorkDTO(BaseModel):
    start_time: str
    end_time: str
    organization: str
    post: str
    duties: str
    sphere: str


class ResumeDTO(BaseModel):
    name: constr(max_length=50)  # Устанавливаем ограничение на длину
    study: Optional[StudyDTO] = None
    desired_busyness: List[str] = []
    specialization: List[str] = []
    skills: List[str] = []
    about_me: Optional[constr(max_length=1000)] = None
    courses: List[CourseDTO] = []
    work_experience: List[WorkDTO] = []

