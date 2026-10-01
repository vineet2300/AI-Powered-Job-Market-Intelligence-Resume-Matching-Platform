from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from backend.database import engine
from backend.schemas import JobCreate, JobUpdate
from backend.services.job_classifier import classify_job


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


# =========================================================
# GET ALL JOBS
# =========================================================

@router.get("/")
def get_jobs():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    id,
                    title,
                    company,
                    location,
                    description,
                    skills,
                    salary_min,
                    salary_max,
                    role_category,
                    sector,
                    job_type,
                    experience_min,
                    experience_max,
                    source,
                    external_id,
                    source_url,
                    recruiter_email,
                    posted_at,
                    fetched_at,
                    created_at
                FROM jobs
                ORDER BY id DESC
            """)
        )

        jobs = []

        for row in result:

            jobs.append({
                "id": row.id,
                "title": row.title,
                "company": row.company,
                "location": row.location,
                "description": row.description,
                "skills": row.skills,
                "salary_min": row.salary_min,
                "salary_max": row.salary_max,

                "role_category": row.role_category,
                "sector": row.sector,
                "job_type": row.job_type,

                "experience_min": row.experience_min,
                "experience_max": row.experience_max,

                "source": row.source,
                "external_id": row.external_id,
                "source_url": row.source_url,
                "recruiter_email": row.recruiter_email,

                "posted_at": row.posted_at,
                "fetched_at": row.fetched_at,
                "created_at": row.created_at
            })

        return jobs


# =========================================================
# CREATE JOB
# Recruiter manually posts a job
# Automatically classify role from job title
# =========================================================

@router.post("/")
def create_job(job: JobCreate):

    # Automatically detect role category
    role_category = classify_job(job.title)

    with engine.begin() as connection:

        result = connection.execute(
            text("""
                INSERT INTO jobs
                (
                    title,
                    company,
                    location,
                    description,
                    skills,
                    salary_min,
                    salary_max,
                    recruiter_email,
                    role_category,
                    source
                )
                VALUES
                (
                    :title,
                    :company,
                    :location,
                    :description,
                    :skills,
                    :salary_min,
                    :salary_max,
                    :recruiter_email,
                    :role_category,
                    :source
                )
                RETURNING id
            """),
            {
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "description": job.description,
                "skills": job.skills,
                "salary_min": job.salary_min,
                "salary_max": job.salary_max,
                "recruiter_email": str(job.recruiter_email),

                "role_category": role_category,
                "source": "recruiter"
            }
        )

        new_id = result.scalar()

    return {
        "message": "Job added successfully",
        "job_id": new_id,
        "role_category": role_category
    }


# =========================================================
# GET SINGLE JOB
# =========================================================

@router.get("/{job_id}")
def get_job(job_id: int):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    id,
                    title,
                    company,
                    location,
                    description,
                    skills,
                    salary_min,
                    salary_max,
                    role_category,
                    sector,
                    job_type,
                    experience_min,
                    experience_max,
                    source,
                    external_id,
                    source_url,
                    recruiter_email,
                    posted_at,
                    fetched_at,
                    created_at
                FROM jobs
                WHERE id = :job_id
            """),
            {
                "job_id": job_id
            }
        )

        row = result.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )

        return {
            "id": row.id,
            "title": row.title,
            "company": row.company,
            "location": row.location,
            "description": row.description,
            "skills": row.skills,
            "salary_min": row.salary_min,
            "salary_max": row.salary_max,

            "role_category": row.role_category,
            "sector": row.sector,
            "job_type": row.job_type,

            "experience_min": row.experience_min,
            "experience_max": row.experience_max,

            "source": row.source,
            "external_id": row.external_id,
            "source_url": row.source_url,
            "recruiter_email": row.recruiter_email,

            "posted_at": row.posted_at,
            "fetched_at": row.fetched_at,
            "created_at": row.created_at
        }


# =========================================================
# UPDATE JOB
# =========================================================

@router.put("/{job_id}")
def update_job(
    job_id: int,
    job: JobUpdate
):

    # Recalculate role if job title changes
    role_category = classify_job(job.title)

    with engine.begin() as connection:

        result = connection.execute(
            text("""
                UPDATE jobs
                SET
                    title = :title,
                    company = :company,
                    location = :location,
                    description = :description,
                    skills = :skills,
                    salary_min = :salary_min,
                    salary_max = :salary_max,
                    role_category = :role_category
                WHERE id = :job_id
            """),
            {
                "job_id": job_id,

                "title": job.title,
                "company": job.company,
                "location": job.location,
                "description": job.description,
                "skills": job.skills,

                "salary_min": job.salary_min,
                "salary_max": job.salary_max,

                "role_category": role_category
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )

    return {
        "message": "Job updated successfully",
        "role_category": role_category
    }


# =========================================================
# DELETE JOB
# =========================================================

@router.delete("/{job_id}")
def delete_job(job_id: int):

    with engine.begin() as connection:

        result = connection.execute(
            text("""
                DELETE FROM jobs
                WHERE id = :job_id
            """),
            {
                "job_id": job_id
            }
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )

    return {
        "message": "Job deleted successfully"
    }