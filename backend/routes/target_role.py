from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from sqlalchemy import text
from collections import Counter
import tempfile
import os
import fitz

from backend.database import engine
from backend.services.skill_extractor import extract_skills


router = APIRouter(
    prefix="/target-role",
    tags=["Target Role Analysis"]
)


def extract_pdf_text(file_path):
    document = fitz.open(file_path)

    resume_text = ""

    for page in document:
        resume_text += page.get_text()

    document.close()

    return resume_text


@router.post("/analyze")
async def analyze_target_role(
    role: str = Form(...),
    file: UploadFile = File(...)
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are allowed"
        )

    role = role.strip().lower()

    temp_path = None

    try:

        # Save resume temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(await file.read())
            temp_path = temp_file.name

        resume_text = extract_pdf_text(temp_path)

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract resume text"
            )

        resume_skills = set(
            extract_skills(resume_text)
        )

        # Get jobs belonging to selected role
        with engine.connect() as connection:

            jobs = connection.execute(
                text("""
                    SELECT description
                    FROM jobs
                    WHERE LOWER(TRIM(role_category)) = :role
                    AND description IS NOT NULL
                """),
                {
                    "role": role
                }
            ).fetchall()

        if not jobs:
            raise HTTPException(
                status_code=404,
                detail=(
                    "No jobs found for this role. "
                    "Try another target role."
                )
            )

        # Count skills across job descriptions
        skill_counter = Counter()

        for job in jobs:

            job_skills = set(
                extract_skills(
                    job.description or ""
                )
            )

            skill_counter.update(job_skills)

        if not skill_counter:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Not enough skill information "
                    "found for this role."
                )
            )

        # Top skills observed in current job data
        top_skills = skill_counter.most_common(10)

        target_skills = {
            skill
            for skill, count in top_skills
        }

        matched_skills = (
            resume_skills.intersection(
                target_skills
            )
        )

        missing_skills = (
            target_skills.difference(
                resume_skills
            )
        )

        fit_percentage = (
            len(matched_skills)
            / len(target_skills)
        ) * 100

        # Add frequency information
        market_skills = []

        total_jobs = len(jobs)

        for skill, count in top_skills:

            market_skills.append({
                "skill": skill,
                "job_count": count,
                "percentage_of_jobs": round(
                    (count / total_jobs) * 100,
                    2
                )
            })

        return {
            "target_role": role,
            "jobs_analyzed": total_jobs,
            "current_fit_percentage": round(
                fit_percentage,
                2
            ),
            "matched_skills": sorted(
                matched_skills
            ),
            "missing_skills": sorted(
                missing_skills
            ),
            "important_market_skills":
                market_skills,
            "recommendation": (
                "Focus on the missing skills that "
                "appear frequently in current job "
                "listings. Add them to your resume "
                "only after you have genuinely "
                "learned or demonstrated them "
                "through projects or experience."
            )
        }

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)