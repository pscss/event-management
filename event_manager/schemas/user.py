from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserBase(BaseModel):
    name: str
    email: EmailStr
    country_code: str
    phone_number: str

    @field_validator("phone_number", mode="before")
    def check_valid_phone_number(cls, v: str):
        if not len(v) == 10:
            raise ValueError(
                "Phone number not valid. Please provide a 10 digit number."
            )
        else:
            return v


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None
    country_code: Optional[str] = None
    phone_number: Optional[str] = None


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
