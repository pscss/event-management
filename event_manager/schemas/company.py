from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class CompanyBase(BaseModel):
    name: str
    address: str
    email: EmailStr
    country_code: str
    phone_number: str
    registration_number: str

    @field_validator("phone_number", mode="before")
    def check_valid_phone_number(cls, v: str):
        if not len(v) == 10:
            raise ValueError(
                "Phone number not valid. Please provide a 10 digit number."
            )
        else:
            return v


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    country_code: Optional[str] = None
    phone_number: Optional[str] = None


class Company(CompanyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
