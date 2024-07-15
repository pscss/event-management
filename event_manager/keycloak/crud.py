from logging import getLogger
from typing import Optional

from keycloak import KeycloakAdmin, KeycloakGetError, KeycloakOpenIDConnection

from event_manager.core.config import settings
from event_manager.keycloak.permission_definitions import Roles

logger = getLogger(__name__)


keycloak_connection = KeycloakOpenIDConnection(
    server_url=settings.KEYCLOAK_URL,
    username=settings.KEYCLOAK_USERNAME,
    password=settings.KEYCLOAK_ADMIN_PASSWORD,
    realm_name=settings.KEYCLOAK_REALM,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
    verify=True,
)

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
        logger.info(f"User count after creating {count_users}")
        roles = await keycloak_admin.a_get_realm_roles()
        logger.info(f"Keycloak roles --> {roles}")
        if is_admin:
            final_role = next(role for role in roles if role["name"] == "admin")
        else:
            final_role = next(role for role in roles if role["name"] == "user")
        await keycloak_admin.a_assign_realm_roles(user_id=user_id, roles=[final_role])
        return user_id
    except KeycloakGetError:
        raise
    except StopIteration:
        raise RuntimeError("No role with name 'admin' found")
    except Exception as e:
        logger.exception("Error occurred during creating user in keycloak")
        raise e


async def update_keycloak_user(
    user_id: str,
    username: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
    role: Optional[Roles] = None,
    old_role: Optional[Roles] = None,
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
        await keycloak_admin.a_update_user(user_id=user_id, payload=user)
        if role:
            roles = await keycloak_admin.a_get_realm_roles()
            logger.info(f"Keycloak roles --> {roles}")
            update_role = next(
                krole for krole in roles if krole["name"] == role.value.lower()
            )
            delete_role = next(
                krole for krole in roles if krole["name"] == old_role.value.lower()
            )
            logger.debug(f"OLD ROLE --> {delete_role}")
            await keycloak_admin.a_delete_realm_roles_of_user(
                user_id=user_id, roles=[delete_role]
            )
            await keycloak_admin.a_assign_realm_roles(
                user_id=user_id, roles=[update_role]
            )
    except StopIteration:
        raise RuntimeError(f"No role with name {role.value} found")
    except Exception as e:
        logger.exception("Error occurred during updating user in keycloak")
        raise e


async def delete_keycloak_user(user_id: str) -> None:
    try:
        resp = await keycloak_admin.a_delete_user(user_id=user_id)
        logger.info(f"keycloak delete response {resp}")
        count_users = await keycloak_admin.a_users_count()
        logger.info(f"User count after deleting {count_users}")
    except Exception as e:
        logger.exception(f"Error while deleting keycloak user with id {user_id}")
        raise e
