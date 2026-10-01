import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()


# -----------------------------
# LOCAL DATABASE CONNECTION
# -----------------------------
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

LOCAL_DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# -----------------------------
# NEON DATABASE CONNECTION
# -----------------------------
NEON_DATABASE_URL = os.getenv("NEON_DATABASE_URL")

if not NEON_DATABASE_URL:
    raise ValueError(
        "NEON_DATABASE_URL is not set. "
        "Set it in the PowerShell terminal before running this script."
    )

if NEON_DATABASE_URL.startswith("postgresql://"):
    NEON_DATABASE_URL = NEON_DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg2://",
        1,
    )


local_engine = create_engine(
    LOCAL_DATABASE_URL,
    pool_pre_ping=True,
)

neon_engine = create_engine(
    NEON_DATABASE_URL,
    pool_pre_ping=True,
)


def migrate_jobs():
    print("Starting job migration...")

    with local_engine.connect() as local_connection:
        result = local_connection.execute(
            text("SELECT * FROM jobs ORDER BY id")
        )

        jobs = result.mappings().all()

    print(f"Jobs found in local database: {len(jobs)}")

    if not jobs:
        print("No jobs found. Nothing to migrate.")
        return

    inserted = 0
    skipped = 0

    with neon_engine.begin() as neon_connection:

        for job in jobs:

            existing = neon_connection.execute(
                text(
                    """
                    SELECT id
                    FROM jobs
                    WHERE id = :id
                    """
                ),
                {"id": job["id"]},
            ).first()

            if existing:
                skipped += 1
                continue

            columns = list(job.keys())

            column_names = ", ".join(columns)

            parameter_names = ", ".join(
                f":{column}" for column in columns
            )

            query = text(
                f"""
                INSERT INTO jobs ({column_names})
                VALUES ({parameter_names})
                """
            )

            neon_connection.execute(
                query,
                dict(job),
            )

            inserted += 1

    print()
    print("Migration completed!")
    print(f"Inserted: {inserted}")
    print(f"Skipped: {skipped}")

    with neon_engine.connect() as neon_connection:
        total = neon_connection.execute(
            text("SELECT COUNT(*) FROM jobs")
        ).scalar()

    print(f"Total jobs in Neon: {total}")


if __name__ == "__main__":
    migrate_jobs()