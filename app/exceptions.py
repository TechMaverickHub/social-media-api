from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled, PermissionDenied
from django.conf import settings

from app.global_constants import ErrorMessage
from app.utils import get_response_schema


def custom_exception_handler(exc, context):
    if isinstance(exc, Throttled):
        wait_time = int(exc.wait) if hasattr(exc, 'wait') else None
        message = ErrorMessage.THROTTLE_LIMIT_EXCEEDED.value
        if wait_time:
            message += f" Try again in {wait_time} seconds."

        return_data = {
            settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: [message]
        }
        return get_response_schema(return_data, ErrorMessage.THROTTLE_LIMIT_EXCEEDED.value, status.HTTP_429_TOO_MANY_REQUESTS)

    if isinstance(exc, PermissionDenied):
        return get_response_schema({}, ErrorMessage.FORBIDDEN.value, status.HTTP_403_FORBIDDEN)

    return exception_handler(exc, context)
