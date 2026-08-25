import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Get the folder where database.py is located
BASE_DIR = Path(__file__).resolve().parent

# Explicitly select backend/.env
ENV_FILE = BASE_DIR / ".env"

# Load that exact .env file
load_dotenv(ENV_FILE, override=True)

DATABASE_URL = os.getenv("DATABASE_URL")

print("======================================")
print("Loading database configuration")
print("ENV FILE:", ENV_FILE)
print("DATABASE URL:", DATABASE_URL)
print("======================================")


if not DATABASE_URL:
    raise ValueError("DATABASE_URL was not found in backend/.env")


engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()