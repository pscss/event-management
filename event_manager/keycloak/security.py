from typing import TYPE_CHECKING, Type

from fastapi import Depends

from event_manager.keycloak.exceptions import AuthorizationException
from event_manager.keycloak.permissions import role_has_permission
from event_manager.keycloak.utils import (
    get_auth_token,
    read_role_from_token,
    validate_and_parse_token,
)

if TYPE_CHECKING:
    from event_manager.keycloak.permissions import SimplePermissionClass

from logging import getLogger

logger = getLogger(__name__)


async def get_parsed_token(token: str = Depends(get_auth_token)) -> dict:
    return await validate_and_parse_token(token)


class IsAuthorized:
    def __init__(self, permission: Type["SimplePermissionClass"]):
        self.permission = permission

    def __call__(self, parsed_token: dict = Depends(get_parsed_token)) -> None:
        role = read_role_from_token(parsed_token)
        logger.info(f"ROLE --> { role}")
        logger.info(f"Allowed Permissions --> { self.permission.allowed_permission}")
        assert self.permission.allowed_permission, "Allowed permission missing"
        if not role_has_permission(role, self.permission.allowed_permission):
            raise AuthorizationException(detail=self.permission.message)
