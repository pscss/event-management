from typing import TYPE_CHECKING

from sqlalchemy import VARCHAR, Column, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from event_manager.models.base import Base

if TYPE_CHECKING:
    from event_manager.models.user import User


class Company(Base):
    __tablename__ = "companies"
    __table_args__ = (
        UniqueConstraint("name", "email", name="company_name_email_uix"),
        UniqueConstraint("phone_number", name="company_phone_number_uix"),
        Index("company_name_email_idx", "name", "email"),
    )
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    country_code: str = Column(String, nullable=False)
    phone_number: str = Column(VARCHAR, nullable=False, index=True)
    registration_number = Column(String, nullable=False, unique=True)

    users: Mapped[list["User"]] = relationship(
        "User", back_populates="company", lazy="selectin"
    )
