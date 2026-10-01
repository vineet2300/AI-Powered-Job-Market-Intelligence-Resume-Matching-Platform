import os
import requests
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import text

from backend.database import engine
from backend.services.job_classifier import classify_job

load_dotenv()

JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY")


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


def fetch_jooble_jobs(
    role,
    location="India",
    results_per_page=20
):

    url = f"https://jooble.org/api/{JOOBLE_API_KEY}"

    payload = {
        "keywords": role,
        "location": location,
        "page": 1,
        "ResultOnPage": results_per_page
    }

    response = requests.post(
        url,
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return data.get("jobs", [])


def save_jooble_jobs(jobs, role):

    added_jobs = 0
    skipped_jobs = 0

    with engine.begin() as connection:

        for job in jobs:

            # Jooble link is used as external identifier
            source_url = job.get("link")

            if not source_url:
                continue

            external_id = source_url.rstrip("/").split("/")[-1]

            # Check duplicate inside Jooble jobs
            existing_job = connection.execute(
                text("""
                    SELECT id
                    FROM jobs
                    WHERE source = :source
                    AND external_id = :external_id
                """),
                {
                    "source": "jooble",
                    "external_id": external_id
                }
            ).fetchone()

            if existing_job:
                skipped_jobs += 1
                continue

            company = job.get("company") or "Unknown Company"
            location = job.get("location") or "India"
            job_type = job.get("type") or None

            connection.execute(
                text("""
                    INSERT INTO jobs
                    (
                        title,
                        company,
                        location,
                        description,
                        source,
                        role_category,
                        external_id,
                        source_url,
                        job_type,
                        posted_at,
                        fetched_at
                    )
                    VALUES
                    (
                        :title,
                        :company,
                        :location,
                        :description,
                        :source,
                        :role_category,
                        :external_id,
                        :source_url,
                        :job_type,
                        :posted_at,
                        :fetched_at
                    )
                """),
                {
                    "title": job.get(
                        "title",
                        "Unknown Job"
                    ),
                    "company": company,
                    "location": location,
                    "description": job.get("snippet"),
                    "source": "jooble",
                    "role_category": classify_job(
                        job.get("title", "")
                    ),
                    "external_id": external_id,
                    "source_url": source_url,
                    "job_type": job_type,
                    "posted_at": job.get("updated"),
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

        print(f"\nFetching Jooble: {role}")

        try:

            jobs = fetch_jooble_jobs(
                role=role,
                location="India",
                results_per_page=20
            )

            added, skipped = save_jooble_jobs(
                jobs,
                role
            )

            total_fetched += len(jobs)
            total_added += added
            total_skipped += skipped

            print("Fetched:", len(jobs))
            print("Saved:", added)
            print("Duplicates:", skipped)

        except Exception as error:

            print(
                f"Error fetching {role}: {error}"
            )

    print("\n" + "=" * 50)
    print("JOOBLE FETCH COMPLETE")
    print("=" * 50)

    print("Total fetched:", total_fetched)
    print("New jobs saved:", total_added)
    print("Duplicates skipped:", total_skipped)


if __name__ == "__main__":

    fetch_multiple_roles()