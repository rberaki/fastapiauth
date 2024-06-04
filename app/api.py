from fastapi import FastAPI, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_database
from .models import User

app = FastAPI()


@app.get("/users/")
async def read_users(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(User))
    return result.scalars().all()
