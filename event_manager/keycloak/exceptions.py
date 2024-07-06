from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN


class AuthenticationException(HTTPException):
    """
    Base for all the Authentication Exceptions.
    For historical reasons, the default status code will be 403 instead of 401.
    """

    def __init__(
        self, status_code: int = HTTP_403_FORBIDDEN, detail: str = "Unauthorized"
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)


class MissingTokenException(AuthenticationException):
    """Raised when no access token is found on the request"""

    def __init__(self) -> None:
        super().__init__(detail="No access token provided")


class TokenExpiredException(AuthenticationException):
    """Raised when the decoded token has expired"""

    def __init__(self) -> None:
        super().__init__(detail="Token expired")


class TokenDecodingException(AuthenticationException):
    """Raised when token decoding fails for some other reason"""

    def __init__(self) -> None:
        super().__init__(detail="Token could not be decoded")


class TokenReadException(AuthenticationException):
    """Raised when token misses mandatory information"""

    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Token could not be read: {message}",
        )


class AuthorizationException(HTTPException):
    """Raised when a request is not authorized to perform the request"""

    def __init__(
        self, status_code: int = HTTP_403_FORBIDDEN, detail: str | None = "Forbidden"
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
