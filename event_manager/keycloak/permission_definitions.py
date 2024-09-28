import enum
from typing import Optional


@enum.unique
class Permission(enum.Enum):
    VIEW_EVENT = "VIEW_EVENT"
    MAKE_BOOKING = "MAKE_BOOKING"
    DO_PAYMENT = "DO_PAYMENT"
    CREATE_EVENT = "CREATE_EVENT"
    DELETE_EVENT = "DELETE_EVENT"
    MANAGE_USERS = "MANAGE_USERS"


@enum.unique
class Roles(enum.Enum):
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"
    USER = "USER"


permissions_user = [
    Permission.VIEW_EVENT,
    Permission.MAKE_BOOKING,
    Permission.DO_PAYMENT,
]

permissions_admin = permissions_user + [
    Permission.CREATE_EVENT,
    Permission.DELETE_EVENT,
]

permissions_super_admin = (
    permissions_user + permissions_admin + [Permission.MANAGE_USERS]
)

role_to_permissions_map = {
    "user": permissions_user,
    "admin": permissions_admin,
    "super_admin": permissions_super_admin,
}


def permissions_for_role(r: Optional[str]) -> list[Permission]:
    if not r:
        return []
    elif r in role_to_permissions_map:
        return role_to_permissions_map[r]
    raise Exception(f"Role could not be recognized {r}")


def role_has_permission(role: str, permission: Permission) -> bool:
    try:
        return permission in permissions_for_role(role)
    except Exception:
        return False
