from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import User
from .schemas import UserEdit
from .crypt import hash_password


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self):
        result = await self.db_session.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, id: int):
        result = await self.db_session.execute(select(User).filter(User.id == id))
        return result.scalar_one_or_none()

    async def create(self, user: UserEdit):
        password = hash_password(user.password)
        new_user = User(firstname=user.firstname,
                        lastname=user.lastname,
                        email_address=user.email_address,
                        username=user.username,
                        password=password)
        self.db_session.add(new_user)
        await self.db_session.commit()
        await self.db_session.refresh(new_user)
        return new_user

    async def update(self, usr_from_db: User, user: UserEdit):
        usr_from_db.username = user.username
        usr_from_db.firstname = user.firstname
        usr_from_db.lastname = user.lastname
        usr_from_db.password = hash_password(user.password)
        await self.db_session.commit()
        await self.db_session.refresh(usr_from_db)
        return usr_from_db

    async def delete(self, user: User):
        await self.db_session.delete(user)
        await self.db_session.commit()
