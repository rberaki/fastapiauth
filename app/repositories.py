from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import User
from .schemas import UserCreate, UserUpdate
from .auth import get_password_hash, verify_password


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self):
        result = await self.db_session.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, id: int):
        result = await self.db_session.execute(select(User).filter(User.id == id))
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str):
        result = await self.db_session.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none()

    async def create(self, user: UserCreate):
        password = get_password_hash(user.password)
        new_user = User(firstname=user.firstname,
                        lastname=user.lastname,
                        email_address=user.email_address,
                        username=user.username,
                        password=password)
        self.db_session.add(new_user)
        await self.db_session.commit()
        await self.db_session.refresh(new_user)
        return new_user

    async def update(self, usr_from_db: User, user: UserUpdate):
        usr_from_db.username = user.username
        usr_from_db.firstname = user.firstname
        usr_from_db.lastname = user.lastname
        if user.password:
            usr_from_db.password = get_password_hash(user.password)
        await self.db_session.commit()
        await self.db_session.refresh(usr_from_db)
        return usr_from_db

    async def delete(self, user: User):
        await self.db_session.delete(user)
        await self.db_session.commit()

    async def authenticate(self, username: str, password: str):
        usr_from_db = await self.get_by_username(username)
        if usr_from_db and verify_password(password, usr_from_db.password):
            return usr_from_db
        return None
