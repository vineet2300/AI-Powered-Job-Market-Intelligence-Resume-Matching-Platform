import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

# Production me DATABASE_URL (Neon/Vercel) use hogi.
# Local development me existing DB_HOST, DB_PORT etc. use honge.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    DATABASE_URL = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

# Neon connection strings normally start with postgresql://
# SQLAlchemy + psycopg2 ke liye explicit driver set kar rahe hain.
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg2://",
        1,
    )


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT current_database();")
            )

            database_name = result.scalar()

            print("Database connected successfully!")
            print("Connected database:", database_name)

    except Exception as error:
        print("Database connection failed!")
        print(error)


if __name__ == "__main__":
    test_connection()