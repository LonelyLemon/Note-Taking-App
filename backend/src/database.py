import os

from sqlalchemy import engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRESQL_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRESQL_HOST")
POSTGRES_PORT = os.getenv("POSTGRESQL_PORT")
POSTGRES_DB = os.getenv("POSTGRESQL_DB")

SQLALCHEMY_DATABASE_URL = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()