from pydantic import BaseModel, EmailStr


class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    description: str
    skills: str
    salary_min: float
    salary_max: float
    recruiter_email: EmailStr


class JobUpdate(BaseModel):
    title: str
    company: str
    location: str
    description: str
    skills: str
    salary_min: float
    salary_max: float