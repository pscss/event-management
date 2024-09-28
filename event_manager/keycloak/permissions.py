from typing import Any

from event_manager.keycloak.permission_definitions import (
    Permission,
    role_has_permission,
)


class SimplePermissionClass:
    """
    Extend this class to define new permission classes that depend on only one permission
    """

    message = "User is not authorized to access this resource"
    allowed_permission: Permission | None = None

    async def has_permission(self, source: Any, role: str, **kwargs: Any) -> bool:
        if self.allowed_permission is None:
            return False
        return role_has_permission(role, self.allowed_permission)


class CanCreateEvent(SimplePermissionClass):
    message = "User is not authorized to create events"
    allowed_permission = Permission.CREATE_EVENT


class CanMakeBooking(SimplePermissionClass):
    message = "User is not authorized to make bookings"
    allowed_permission = Permission.MAKE_BOOKING


class CanDoPayment(SimplePermissionClass):
    message = "User is not authorized to do payments"
    allowed_permission = Permission.DO_PAYMENT


class CanViewEvent(SimplePermissionClass):
    message = "User is not authorized to view Events"
    allowed_permission = Permission.DELETE_EVENT


class CanManageUser(SimplePermissionClass):
    message = "User is not authorized to C/U/D users"
    allowed_permission = Permission.MANAGE_USERS
