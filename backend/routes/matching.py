from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from sqlalchemy import text

import fitz

from backend.database import engine
from backend.services.matcher import (
    match_resume_with_job
)


router = APIRouter(
    prefix="/matching",
    tags=["Job Matching"]
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
# BEST JOB MATCHING API
# =========================================================

@router.post("/best-jobs")
async def find_best_jobs(
    file: UploadFile = File(...),
    limit: int = 10
):

    # -----------------------------------------------------
    # VALIDATE FILE
    # -----------------------------------------------------

    if file.content_type != "application/pdf":

        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are allowed"
        )


    # -----------------------------------------------------
    # VALIDATE LIMIT
    # -----------------------------------------------------

    if limit < 1 or limit > 50:

        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 50"
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
                detail=(
                    "Could not extract "
                    "text from resume"
                )
            )


        # -------------------------------------------------
        # GET JOBS FROM POSTGRESQL
        # -------------------------------------------------

        with engine.connect() as connection:

            jobs = connection.execute(

                text("""
                    SELECT
                        id,
                        title,
                        company,
                        location,
                        description,
                        role_category,
                        source,
                        source_url
                    FROM jobs
                    WHERE description IS NOT NULL
                """)

            ).mappings().all()


        # -------------------------------------------------
        # MATCH RESUME WITH JOBS
        # -------------------------------------------------

        results = []


        for job in jobs:

            match = match_resume_with_job(
                resume_text,
                job["description"] or "",
                job["title"] or ""
            )


            # Ignore jobs where no recognizable
            # skills were detected
            if not match["job_skills"]:
                continue


            results.append({

                "job_id":
                    job["id"],

                "title":
                    job["title"],

                "company":
                    job["company"],

                "location":
                    job["location"],

                "role_category":
                    job["role_category"],

                "source":
                    job["source"],

                "source_url":
                    job["source_url"],


                # -----------------------------------------
                # COMPATIBILITY
                # -----------------------------------------

                "match_percentage":
                    match[
                        "match_percentage"
                    ],

                "skill_match_percentage":
                    match[
                        "skill_match_percentage"
                    ],

                "evidence_confidence":
                    match[
                        "evidence_confidence"
                    ],


                # -----------------------------------------
                # COUNTS
                # -----------------------------------------

                "matched_skill_count":
                    match[
                        "matched_skill_count"
                    ],

                "detected_job_skill_count":
                    match[
                        "detected_job_skill_count"
                    ],


                # -----------------------------------------
                # EXPLANATION
                # -----------------------------------------

                "why_match":
                    match[
                        "why_match"
                    ],


                # -----------------------------------------
                # SKILLS
                # -----------------------------------------

                "matched_skills":
                    match[
                        "matched_skills"
                    ],

                "missing_skills":
                    match[
                        "missing_skills"
                    ],

                "job_skills":
                    match[
                        "job_skills"
                    ]
            })


        # -------------------------------------------------
        # RANK JOBS
        # -------------------------------------------------

        results.sort(

            key=lambda job: (

                job[
                    "match_percentage"
                ],

                job[
                    "matched_skill_count"
                ],

                job[
                    "detected_job_skill_count"
                ]

            ),

            reverse=True
        )


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return {

            "jobs_analyzed":
                len(jobs),

            "jobs_with_detected_skills":
                len(results),

            "top_matches":
                results[:limit]
        }


    except HTTPException:
        raise


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to match resume: {str(error)}"
        )