from enum import Enum


class ErrorCodes(Enum):
    USER_ALREADY_EXISTS = "User already exists with this social ID"
    USER_NOT_FOUND = "User not found"
    INVALID_TOKEN = "Invalid token"
    DATABASE_ERROR = "Database operation failed"
    UNAUTHORIZED = "Unauthorized access"


class ErrorDetails(Enum):
    USER_ALREADY_EXISTS = {
        "message": "A user with this social ID already exists.",
        "status_code": 400
    }
    USER_NOT_FOUND = {
        "message": "The specified user was not found.",
        "status_code": 404
    }
    INVALID_TOKEN = {
        "message": "The provided token is invalid.",
        "status_code": 401
    }
    DATABASE_ERROR = {
        "message": "An error occurred while accessing the database.",
        "status_code": 500
    }
    UNAUTHORIZED = {
        "message": "You are not authorized to perform this action.",
        "status_code": 403
    }
