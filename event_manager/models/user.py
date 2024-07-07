from typing import TYPE_CHECKING

from sqlalchemy import VARCHAR, Column, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from event_manager.models.base import Base

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

    bookings: Mapped["Booking"] = relationship("Booking", back_populates="user")
