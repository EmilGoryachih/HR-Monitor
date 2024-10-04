from typing import Optional, List
from pydantic import BaseModel


from models.dbModels.Vacancy.vacancy import Experience, Busyness


class VacancyDTO(BaseModel):
    name: str
    description: Optional[str]
    salary: Optional[int]
    experience: Optional[Experience]
    busyness: Optional[List[Busyness]]
