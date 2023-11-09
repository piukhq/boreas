class InvalidTokenError(Exception):
    status_code = 401
    content = {
        "detail": [
            {
                "msg": "Authentication failed",
                "type": "Unauthorized",
            }
        ]
    }
