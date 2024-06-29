from sqlalchemy import VARCHAR, Column, Index, String, UniqueConstraint
from sqlalchemy.orm import relationship

from event_manager.models.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("name", "email", name="name_email_uix"),
        UniqueConstraint("phone_number", name="phone_number_uix"),
        Index("name", "email"),
    )
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    country_code = Column(String, nullable=False)
    phone_number = Column(VARCHAR, nullable=False, index=True)

    bookings = relationship("Booking", back_populates="user")
