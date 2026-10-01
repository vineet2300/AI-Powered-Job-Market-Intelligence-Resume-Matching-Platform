from sqlalchemy import text

from backend.database import engine


def classify_job(title):

    if not title:
        return "other"

    title = title.lower()

    # Data Analyst
    if "data analyst" in title:
        return "data analyst"

    # Business Analyst
    if "business analyst" in title:
        return "business analyst"

    # Data Scientist
    if "data scientist" in title:
        return "data scientist"

    # Machine Learning
    if (
        "machine learning" in title
        or "ml engineer" in title
        or "ai engineer" in title
    ):
        return "machine learning engineer"

    # DevOps
    if (
        "devops" in title
        or "dev ops" in title
        or "site reliability engineer" in title
        or "sre engineer" in title
    ):
        return "devops engineer"

    # Cyber Security
    if (
        "cyber security" in title
        or "cybersecurity" in title
        or "security analyst" in title
        or "security engineer" in title
    ):
        return "cyber security"

    # Cloud
    if (
        "cloud engineer" in title
        or "cloud developer" in title
        or "cloud architect" in title
    ):
        return "cloud engineer"

    # Full Stack
    if (
        "full stack" in title
        or "fullstack" in title
    ):
        return "full stack developer"

    # Frontend
    if (
        "frontend" in title
        or "front end" in title
        or "react developer" in title
        or "angular developer" in title
    ):
        return "frontend developer"

    # Backend
    if (
        "backend" in title
        or "back end" in title
    ):
        return "backend developer"

    # Python
    if "python" in title:
        return "python developer"

    # Java
    if (
        "java developer" in title
        or "java engineer" in title
    ):
        return "java developer"

    # Software Engineering
    if (
        "software engineer" in title
        or "software developer" in title
        or "application developer" in title
    ):
        return "software engineer"

    return "other"


def classify_existing_jobs():

    updated = 0

    with engine.begin() as connection:

        jobs = connection.execute(
            text("""
                SELECT id, title
                FROM jobs
            """)
        ).fetchall()

        for job in jobs:

            category = classify_job(job.title)

            connection.execute(
                text("""
                    UPDATE jobs
                    SET role_category = :category
                    WHERE id = :job_id
                """),
                {
                    "category": category,
                    "job_id": job.id
                }
            )

            updated += 1

    print("\nJob classification complete!")
    print("Jobs classified:", updated)


if __name__ == "__main__":
    classify_existing_jobs()