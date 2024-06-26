from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from .bearer import JwtBearer
from .database import get_database
from .schemas import User, UserCreate, UserUpdate, Token, UserLogin
from .repositories import UserRepository
from .auth import create_access_token, decode_access_token
from . import TOKEN_EXPIRE_MINUTES

app = FastAPI()


async def get_current_user(token: str = Depends(JwtBearer()), db_session: AsyncSession = Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except InvalidTokenError:
        raise credentials_exception
    user = await UserRepository(db_session).get_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


@app.post("/token", response_model=Token, tags=["Token"])
async def login_for_access_token(user_login: UserLogin, db_session: AsyncSession = Depends(get_database)):
    user = await UserRepository(db_session).authenticate(user_login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    expire_mins = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=expire_mins)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User, tags=["Users"])
async def read_self(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/users/", dependencies=[Depends(JwtBearer())], response_model=list[User], tags=["Users"])
async def read_users(db_session: AsyncSession = Depends(get_database)):
    return await UserRepository(db_session).get_all()


@app.get("/users/{id}", dependencies=[Depends(JwtBearer())], response_model=User, tags=["Users"])
async def read_user(id: int, db_session=Depends(get_database)):
    user = await UserRepository(db_session).get_by_id(id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.post("/users/", response_model=User, tags=["Users"])
async def create_user(user: UserCreate, db_session: AsyncSession = Depends(get_database)):
    return await UserRepository(db_session).create(user)


@app.put("/users/{id}", dependencies=[Depends(JwtBearer())], response_model=User, tags=["Users"])
async def update_user(id: int, user: UserUpdate, db_session: AsyncSession = Depends(get_database)):
    repo = UserRepository(db_session)
    user_from_db = await repo.get_by_id(id)
    if user_from_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await repo.update(user_from_db, user)


@app.delete("/users/{id}", dependencies=[Depends(JwtBearer())], tags=["Users"])
async def delete_user(id: int, db_session: AsyncSession = Depends(get_database)):
    repo = UserRepository(db_session)
    user = await repo.get_by_id(id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await repo.delete(user)
    return {"detail": "User deleted"}
