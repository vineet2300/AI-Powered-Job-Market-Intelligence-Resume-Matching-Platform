from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)

    company = Column(String(200), nullable=False)

    location = Column(String(200))

    description = Column(Text)

    skills = Column(Text)

    
    salary_min = Column(Float)

    salary_max = Column(Float)

    role_category = Column(String(200))

    
    sector = Column(String(200))

    job_type = Column(String(100))

    experience_min = Column(Float)

    experience_max = Column(Float)

    
    source = Column(String(100), default="recruiter")

    external_id = Column(String(255))

    source_url = Column(Text)

    recruiter_email = Column(String(255))

    
    posted_at = Column(DateTime)

    fetched_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)