from logging import getLogger
from typing import Annotated, Optional

import jwt
from fastapi import Depends, WebSocket
from fastapi.security import OAuth2AuthorizationCodeBearer
from jwt import PyJWKClient
from starlette.requests import Request

from event_manager.core.config import settings
from event_manager.keycloak.exceptions import (
    MissingTokenException,
    TokenDecodingException,
    TokenExpiredException,
    TokenReadException,
)
from event_manager.keycloak.permission_definitions import role_to_permissions_map

logger = getLogger(__name__)

JWKS_URI = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"

oauth_2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token",
    refreshUrl=f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token",
)


async def get_auth_token(request: Request = None, websocket: WebSocket = None) -> str:
    """
    Get the Auth token from the request, raises HTTPException if no auth token is present
    """

    headers_source = request or websocket
    assert headers_source
    authorization: Optional[str] = headers_source.headers.get("Authorization")
    if not authorization:
        raise MissingTokenException

    try:
        prefix, token = authorization.strip().split(" ", 1)
    except Exception:
        raise TokenDecodingException

    if prefix != "Bearer":
        raise MissingTokenException

    return token


async def validate_and_parse_token(
    access_token: Annotated[str, Depends(oauth_2_scheme)]
):
    jwks_client = PyJWKClient(JWKS_URI)
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        logger.info(f"SIGN KEY {signing_key.key}")
        decoded_token = jwt.decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_exp": True},
        )
        logger.info(f"DATA {decoded_token}")
        return decoded_token
    except jwt.exceptions.ExpiredSignatureError as e:
        logger.exception("Expired signature")
        raise TokenExpiredException from e
    except jwt.exceptions.InvalidKeyError as e:
        logger.exception("Expired token")
        raise TokenDecodingException from e
    except jwt.exceptions.InvalidSignatureError as e:
        logger.exception("Invalid signature")
        raise TokenDecodingException from e
    except jwt.exceptions.DecodeError as e:
        logger.exception("Exception decoding token")
        raise TokenDecodingException from e
    except Exception as e:
        logger.exception("Exception parsing token", str(e))
        raise TokenDecodingException from e


def reorder_roles(roles: list[str]):
    # Define the priority order
    priority = {"admin": 1, "user": 2}

    # Sort roles based on the priority; roles not in priority will retain their order
    sorted_roles = sorted(roles, key=lambda role: priority.get(role, float("inf")))

    return sorted_roles


def read_role_from_token(parsed_token: dict) -> str:
    all_roles = parsed_token.get("realm_access", {}).get("roles", [])

    if len(all_roles) == 0:
        logger.critical("Keycloak user had no role supplied", parsed_token=parsed_token)
        raise TokenReadException("No role supplied on the user")

    return reorder_roles(all_roles)[0]


async def get_permissions_for_role(role: str) -> list[str]:
    permissions = role_to_permissions_map.get(role, [])
    return [str(p.value) for p in permissions]
