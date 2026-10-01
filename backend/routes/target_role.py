from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from sqlalchemy import text
from collections import Counter
import fitz

from backend.database import engine
from backend.services.skill_extractor import extract_skills


router = APIRouter(
    prefix="/target-role",
    tags=["Target Role Analysis"]
)


# =========================================================
# EXTRACT PDF TEXT
# =========================================================

def extract_pdf_text(pdf_bytes: bytes):

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    resume_text = ""

    for page in document:
        resume_text += page.get_text()

    document.close()

    return resume_text


# =========================================================
# TARGET ROLE ANALYSIS
# =========================================================

@router.post("/analyze")
async def analyze_target_role(
    role: str = Form(...),
    file: UploadFile = File(...)
):

    # -----------------------------------------------------
    # VALIDATE PDF
    # -----------------------------------------------------

    if file.content_type != "application/pdf":

        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are allowed"
        )


    # -----------------------------------------------------
    # VALIDATE ROLE
    # -----------------------------------------------------

    role = role.strip().lower()

    if not role:

        raise HTTPException(
            status_code=400,
            detail="Target role is required"
        )


    try:

        # -------------------------------------------------
        # READ PDF DIRECTLY INTO MEMORY
        # -------------------------------------------------

        file_content = await file.read()

        if not file_content:

            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty"
            )


        # -------------------------------------------------
        # EXTRACT RESUME TEXT
        # -------------------------------------------------

        resume_text = extract_pdf_text(
            file_content
        )

        if not resume_text.strip():

            raise HTTPException(
                status_code=400,
                detail="Could not extract resume text"
            )


        # -------------------------------------------------
        # EXTRACT RESUME SKILLS
        # -------------------------------------------------

        resume_skills = set(
            extract_skills(
                resume_text
            )
        )


        # -------------------------------------------------
        # GET JOBS BELONGING TO SELECTED ROLE
        # -------------------------------------------------

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


        # -------------------------------------------------
        # COUNT SKILLS ACROSS JOB DESCRIPTIONS
        # -------------------------------------------------

        skill_counter = Counter()

        for job in jobs:

            job_skills = set(
                extract_skills(
                    job.description or ""
                )
            )

            skill_counter.update(
                job_skills
            )


        if not skill_counter:

            raise HTTPException(
                status_code=404,
                detail=(
                    "Not enough skill information "
                    "found for this role."
                )
            )


        # -------------------------------------------------
        # TOP SKILLS OBSERVED IN CURRENT JOB DATA
        # -------------------------------------------------

        top_skills = skill_counter.most_common(
            10
        )

        target_skills = {
            skill
            for skill, count in top_skills
        }


        # -------------------------------------------------
        # MATCHED / MISSING SKILLS
        # -------------------------------------------------

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


        # -------------------------------------------------
        # CURRENT FIT
        # -------------------------------------------------

        fit_percentage = (
            len(matched_skills)
            / len(target_skills)
        ) * 100


        # -------------------------------------------------
        # MARKET SKILL FREQUENCY
        # -------------------------------------------------

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


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

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


    except HTTPException:
        raise


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to analyze target role: "
                f"{str(error)}"
            )
        )