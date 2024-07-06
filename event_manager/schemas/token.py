from pydantic import BaseModel, Field


class TokenDetailsBase(BaseModel):
    keycloak_id: str = Field()
    first_name: str = Field()
    last_name: str = Field()
    email: str = Field()
    role: str = Field()


class TokenDetailsWithPermissions(TokenDetailsBase):
    permissions: list = Field(default_factory=list)
