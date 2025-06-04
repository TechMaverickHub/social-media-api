from enum import Enum

class SuccessMessage(str, Enum):

    RECORD_CREATED = "Record created successfully."
    RECORD_RETRIEVED = "Record retrieved successfully."
    RECORD_UPDATED = "Record updated successfully."
    RECORD_DELETED = "Record deleted successfully."


class ErrorMessage(str, Enum):

    SOMETHING_WENT_WRONG = "Something went wrong, please try again."
    BAD_REQUEST = "Bad request."
    FORBIDDEN = "Not authenticated."
    NOT_FOUND = "Resource not found."

class GlobalValues(int, Enum):

    # User Role
    SUPER_ADMIN = 1
    ADMIN = 2
    USER = 3
    MODERATOR = 4


