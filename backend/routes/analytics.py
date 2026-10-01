from fastapi import APIRouter
from sqlalchemy import text
from collections import Counter

from backend.database import engine
from backend.services.skill_extractor import extract_skills


router = APIRouter(
    prefix="/analytics",
    tags=["Job Market Analytics"]
)


@router.get("/overview")
def analytics_overview():

    with engine.connect() as connection:

        # Total jobs
        total_jobs = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM jobs
            """)
        ).scalar()

        # Jobs by role
        role_rows = connection.execute(
            text("""
                SELECT
                    role_category,
                    COUNT(*) AS total
                FROM jobs
                WHERE role_category IS NOT NULL
                GROUP BY role_category
                ORDER BY total DESC
            """)
        ).mappings().all()

        # Jobs by source
        source_rows = connection.execute(
            text("""
                SELECT
                    source,
                    COUNT(*) AS total
                FROM jobs
                WHERE source IS NOT NULL
                GROUP BY source
                ORDER BY total DESC
            """)
        ).mappings().all()

        # Top locations
        location_rows = connection.execute(
            text("""
                SELECT
                    location,
                    COUNT(*) AS total
                FROM jobs
                WHERE location IS NOT NULL
                AND TRIM(location) != ''
                GROUP BY location
                ORDER BY total DESC
                LIMIT 10
            """)
        ).mappings().all()

        # Salary statistics
        salary_data = connection.execute(
            text("""
                SELECT
                    COUNT(*) AS jobs_with_salary,
                    AVG(salary_min) AS avg_salary_min,
                    AVG(salary_max) AS avg_salary_max
                FROM jobs
                WHERE salary_min IS NOT NULL
                OR salary_max IS NOT NULL
            """)
        ).mappings().first()

        # Descriptions for skill analysis
        descriptions = connection.execute(
            text("""
                SELECT description
                FROM jobs
                WHERE description IS NOT NULL
            """)
        ).fetchall()

    # ---------------------------------
    # Skill demand analysis
    # ---------------------------------

    skill_counter = Counter()

    for row in descriptions:

        skills = set(
            extract_skills(
                row.description or ""
            )
        )

        skill_counter.update(skills)

    top_skills = []

    for skill, count in skill_counter.most_common(15):

        top_skills.append({
            "skill": skill,
            "jobs_detected": count,
            "percentage_of_analyzed_jobs": round(
                (
                    count
                    / len(descriptions)
                    * 100
                ),
                2
            ) if descriptions else 0
        })

    # Convert database rows to clean JSON
    jobs_by_role = [
        {
            "role": row["role_category"],
            "jobs": row["total"]
        }
        for row in role_rows
    ]

    jobs_by_source = [
        {
            "source": row["source"],
            "jobs": row["total"]
        }
        for row in source_rows
    ]

    top_locations = [
        {
            "location": row["location"],
            "jobs": row["total"]
        }
        for row in location_rows
    ]

    return {
        "total_jobs": total_jobs,

        "jobs_by_role": jobs_by_role,

        "jobs_by_source": jobs_by_source,

        "top_locations": top_locations,

        "top_detected_skills": top_skills,

        "salary_insights": {
            "jobs_with_salary":
                salary_data["jobs_with_salary"],

            "average_min_salary":
                round(
                    float(
                        salary_data["avg_salary_min"]
                    ),
                    2
                )
                if salary_data["avg_salary_min"]
                is not None
                else None,

            "average_max_salary":
                round(
                    float(
                        salary_data["avg_salary_max"]
                    ),
                    2
                )
                if salary_data["avg_salary_max"]
                is not None
                else None
        },

        "notes": {
            "role_distribution":
                "Shows current job counts by role, "
                "not time-based hiring trends.",

            "skill_detection":
                "Skill percentages represent skills "
                "detected in available job descriptions.",

            "salary":
                "Salary insights use only listings "
                "where salary data is available."
        }
    }