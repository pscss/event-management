from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from event_manager.dal.crud_manager import CRUD
from event_manager.models.user import User
from event_manager.schemas.user import UserCreate, UserUpdate


class UserManager(CRUD[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()


user_manager = UserManager(User)
