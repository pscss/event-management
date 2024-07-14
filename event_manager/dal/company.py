from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from event_manager.dal.crud_manager import CRUD
from event_manager.models.company import Company
from event_manager.schemas.company import CompanyCreate, CompanyUpdate


class CompanyManager(CRUD[Company, CompanyCreate, CompanyUpdate]):
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[Company]:
        result = await db.execute(select(Company).where(Company.email == email))
        return result.scalars().first()


company_manager = CompanyManager(Company)
