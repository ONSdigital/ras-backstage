from functools import wraps
import logging

from structlog import wrap_logger


logger = wrap_logger(logging.getLogger(__name__))


def get_jwt(request):
    def extract_session(original_function):
        @wraps(original_function)
        def extract_session_wrapper(*args, **kwargs):
            encoded_jwt_token = request.headers.get('Authorization')
            if encoded_jwt_token:
                return original_function(encoded_jwt_token, *args, **kwargs)
            else:
                raise Exception
        return extract_session_wrapper
    return extract_session
