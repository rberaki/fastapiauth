from decouple import config
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .models import Base

DB_URL = config('DATABASE_URL')

engine = create_async_engine(DB_URL, echo=True)
SessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


async def get_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        yield session
