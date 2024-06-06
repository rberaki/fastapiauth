from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_database
from .schemas import User, UserCreate, UserUpdate, UserLogin
from .repositories import UserRepository

app = FastAPI()


@app.get("/users/", response_model=list[User])
async def read_users(db_session: AsyncSession = Depends(get_database)):
    return await UserRepository(db_session).get_all()


@app.get("/users/{id}", response_model=User)
async def read_user(id: int, db_session=Depends(get_database)):
    user = await UserRepository(db_session).get_by_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users/", response_model=User)
async def create_user(user: UserCreate, db_session: AsyncSession = Depends(get_database)):
    return await UserRepository(db_session).create(user)


@app.put("/users/{id}", response_model=User)
async def update_user(id: int, user: UserUpdate, db_session: AsyncSession = Depends(get_database)):
    repo = UserRepository(db_session)
    user_from_db = await repo.get_by_id(id)
    if user_from_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await repo.update(user_from_db, user)


@app.delete("/users/{id}")
async def delete_user(id: int, db_session: AsyncSession = Depends(get_database)):
    repo = UserRepository(db_session)
    user = await repo.get_by_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await repo.delete(user)
    return {
        "detail": "User deleted"
    }


@app.post("/user/login/")
async def user_login(user: UserLogin, db_session: AsyncSession = Depends(get_database)):
    repo = UserRepository(db_session)
    user_from_db = await repo.authenticate(user)
    if user_from_db is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "detail": "Login successful"
    }
