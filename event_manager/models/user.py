from typing import TYPE_CHECKING

from sqlalchemy import (
    VARCHAR,
    Column,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, relationship

from event_manager.keycloak.permission_definitions import Roles
from event_manager.models.base import Base
from event_manager.models.company import Company

if TYPE_CHECKING:
    from event_manager.models.booking import Booking


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("name", "email", name="name_email_uix"),
        UniqueConstraint("phone_number", name="phone_number_uix"),
        Index("name", "email"),
    )
    name: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    country_code: str = Column(String, nullable=False)
    phone_number: str = Column(VARCHAR, nullable=False, index=True)
    role: Roles = Column(ENUM(Roles), nullable=False)
    company_id: int = Column(Integer, ForeignKey("companies.id"), nullable=True)
    keycloak_id: str = Column(VARCHAR, nullable=False, index=True)
    username: str = Column(String, nullable=False, index=True)

    company: Mapped["Company"] = relationship(
        "Company", back_populates="users", lazy="selectin"
    )
    bookings: Mapped["Booking"] = relationship(
        "Booking", back_populates="user", lazy="selectin"
    )
