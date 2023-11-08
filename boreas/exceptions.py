"""Custom exceptions for the Boreas API."""

from typing import ClassVar


class InvalidTokenError(Exception):
    """Exception to return on an invalid token."""

    status_code = 401
    content: ClassVar[dict] = {
        "detail": [
            {
                "msg": "Authentication failed",
                "type": "Unauthorized",
            },
        ],
    }
