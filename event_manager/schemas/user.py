from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from event_manager.keycloak.permission_definitions import Roles


class UserBase(BaseModel):
    name: str
    email: EmailStr
    country_code: str
    phone_number: str
    username: str
    role: Optional[Roles] = Roles.USER

    @field_validator("phone_number", mode="before")
    def check_valid_phone_number(cls, v: str):
        if not len(v) == 10:
            raise ValueError(
                "Phone number not valid. Please provide a 10 digit number."
            )
        else:
            return v


class UserCreate(UserBase):
    keycloak_id: Optional[str] = None
    company_id: Optional[int] = None


class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None
    country_code: Optional[str] = None
    phone_number: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
    keycloak_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
