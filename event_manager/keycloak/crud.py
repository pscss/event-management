# keycloak_utils.py
from logging import getLogger
from typing import Optional

from keycloak import KeycloakAdmin, KeycloakGetError, KeycloakOpenIDConnection
from pydantic import BaseModel

from event_manager.core.config import settings

logger = getLogger(__name__)


class KeycloakConfig(BaseModel):
    server_url: str
    username: str
    password: str
    realm_name: str
    client_id: str
    client_secret_key: str


keycloak_config = KeycloakConfig(
    server_url=settings.KEYCLOAK_URL,
    username="aryan",
    password=settings.KEYCLOAK_ADMIN_PASSWORD,
    realm_name=settings.KEYCLOAK_REALM,
    client_id="admin-cli",
    client_secret_key="44eNWbmOfIvyPs8fOrKgrCCqFnPJiJHQ",
)
keycloak_connection = KeycloakOpenIDConnection(
    server_url=settings.KEYCLOAK_URL,
    username="aryan",
    password=settings.KEYCLOAK_ADMIN_PASSWORD,
    realm_name="master",
    user_realm_name=settings.KEYCLOAK_REALM,
    client_id="admin-cli",
    client_secret_key="44eNWbmOfIvyPs8fOrKgrCCqFnPJiJHQ",
    verify=True,
)

# keycloak_admin = KeycloakAdmin(
#     server_url=keycloak_config.server_url,
#     username=keycloak_config.username,
#     password=keycloak_config.password,
#     realm_name=keycloak_config.realm_name,
#     client_secret_key=keycloak_config.client_secret_key,
#     client_id=keycloak_config.client_id,
#     verify=True,
# )
keycloak_admin = KeycloakAdmin(connection=keycloak_connection)


async def create_keycloak_user(
    username: str, email: str, password: str, is_admin: bool = False
) -> str:
    user = {
        "username": username,
        "email": email,
        "enabled": True,
        "credentials": [{"value": password, "type": "password", "temporary": False}],
    }
    logger.info(f"USER --> {user}")
    try:
        user_id = await keycloak_admin.a_create_user(user)
        count_users = await keycloak_admin.a_users_count()
        logger.info(f"User count {count_users}")
    except KeycloakGetError:
        raise
    except Exception as e:
        logger.exception("Error occurred during creating user in keycloak")
        raise e

    if is_admin:
        roles = keycloak_admin.get_realm_roles(search_text="admin")
        logger.info(f"Keycloak roles --> {roles}")
        admin_role = next(role for role in roles if role["name"] == "admin")
        keycloak_admin.assign_realm_roles(user_id=user_id, roles=[admin_role])

    return user_id


def update_keycloak_user(
    user_id: str,
    username: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
):
    user = {}
    if email:
        user["email"] = email
    if username:
        user["username"] = username
    if password:
        user["credentials"] = [
            {"value": password, "type": "password", "temporary": False}
        ]
    try:
        keycloak_admin.update_user(user_id=user_id, payload=user)
    except Exception as e:
        logger.exception("Error occurred during updating user in keycloak")
        raise e


def delete_keycloak_user(user_id: str):
    keycloak_admin.delete_user(user_id=user_id)
