class InvalidTokenError(Exception):
    status_code = 401
    content = {"error_message": "Supplied token is invalid", "error_slug": "INVALID_TOKEN"}
