import os
import requests
from datetime import datetime

from backend.services.job_classifier import classify_job


from dotenv import load_dotenv
from sqlalchemy import text

from backend.database import engine

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")


# Roles that our platform will collect
JOB_ROLES = [
    "data analyst",
    "business analyst",
    "python developer",
    "java developer",
    "software engineer",
    "frontend developer",
    "backend developer",
    "full stack developer",
    "data scientist",
    "machine learning engineer",
    "devops engineer",
    "cloud engineer",
    "cyber security analyst"
]


def fetch_jobs(role, location="India", results_per_page=20):

    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": role,
        "where": location,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    return data.get("results", [])


def save_jobs(jobs, role):

    added_jobs = 0
    skipped_jobs = 0

    with engine.begin() as connection:

        for job in jobs:

            external_id = str(job.get("id"))

            existing_job = connection.execute(
                text("""
                    SELECT id
                    FROM jobs
                    WHERE source = :source
                    AND external_id = :external_id
                """),
                {
                    "source": "adzuna",
                    "external_id": external_id
                }
            ).fetchone()

            if existing_job:
                connection.execute(
        text("""
            UPDATE jobs
            SET role_category = :role
            WHERE source = 'adzuna'
            AND external_id = :external_id
        """),
        {
            "role": classify_job(
                job.get("title", "")
            ),
            "external_id": external_id
        }
    )
                skipped_jobs += 1
                continue

            company = job.get("company", {}).get(
                "display_name",
                "Unknown Company"
            )

            location = job.get("location", {}).get(
                "display_name",
                "India"
            )

            connection.execute(
                text("""
                    INSERT INTO jobs
                    (
                        title,
                        company,
                        location,
                        description,
                        salary_min,
                        salary_max,
                        source,
                        role_category,
                        external_id,
                        source_url,
                        posted_at,
                        fetched_at
                    )
                    VALUES
                    (
                        :title,
                        :company,
                        :location,
                        :description,
                        :salary_min,
                        :salary_max,
                        :source,
                        :role_category,
                        :external_id,
                        :source_url,
                        :posted_at,
                        :fetched_at
                    )
                """),
                {
                    "title": job.get("title", "Unknown Job"),
                    "company": company,
                    "location": location,
                    "description": job.get("description"),
                    "salary_min": job.get("salary_min"),
                    "salary_max": job.get("salary_max"),
                    "source": "adzuna",
                    "role_category": classify_job(
                        job.get("title", "")
                    ),
                    "external_id": external_id,
                    "source_url": job.get("redirect_url"),
                    "posted_at": job.get("created"),
                    "fetched_at": datetime.now()
                }
            )

            added_jobs += 1

    return added_jobs, skipped_jobs


def fetch_multiple_roles():

    total_fetched = 0
    total_added = 0
    total_skipped = 0

    for role in JOB_ROLES:

        print(f"\nFetching: {role}")

        try:
            jobs = fetch_jobs(
                role=role,
                location="India",
                results_per_page=20
            )

            added, skipped = save_jobs(jobs, role)

            total_fetched += len(jobs)
            total_added += added
            total_skipped += skipped

            print("Fetched:", len(jobs))
            print("Saved:", added)
            print("Duplicates:", skipped)

        except Exception as error:
            print(f"Error fetching {role}: {error}")

    print("\n" + "=" * 50)
    print("FETCH COMPLETE")
    print("=" * 50)

    print("Total fetched:", total_fetched)
    print("New jobs saved:", total_added)
    print("Duplicates skipped:", total_skipped)


if __name__ == "__main__":
    fetch_multiple_roles()