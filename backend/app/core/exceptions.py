from fastapi import HTTPException, status


class AutoBotException(HTTPException):
    """Base exception for all AutoBot API errors."""

    def __init__(
        self,
        detail: str = "An unexpected error occurred.",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NotFoundError(AutoBotException):
    """Raised when a requested resource is not found."""

    def __init__(self, detail: str = "Resource not found."):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class PermissionDeniedError(AutoBotException):
    """Raised when the user does not have permission for the requested action."""

    def __init__(self, detail: str = "Permission denied."):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_403_FORBIDDEN,
        )


class ValidationError(AutoBotException):
    """Raised when input validation fails beyond Pydantic's built-in checks."""

    def __init__(self, detail: str = "Validation error."):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


class RateLimitExceededError(AutoBotException):
    """Raised when a client exceeds their rate limit."""

    def __init__(self, detail: str = "Rate limit exceeded. Please try again later."):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            headers={"Retry-After": "60"},
        )
