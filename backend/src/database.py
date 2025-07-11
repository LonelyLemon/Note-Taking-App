import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator

from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRESQL_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRESQL_HOST")
POSTGRES_PORT = os.getenv("POSTGRESQL_PORT")
POSTGRES_DB = os.getenv("POSTGRESQL_DB")

SQLALCHEMY_DATABASE_URL = (f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False, future=True)

SessionLocal: AsyncSession = sessionmaker(
    autoflush=False, 
    autocommit=False, 
    expire_on_commit=False, 
    class_=AsyncSession,
    bind=engine
    )

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session