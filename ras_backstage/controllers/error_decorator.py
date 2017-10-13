import logging
from functools import wraps

from flask import current_app
from ras_backstage.exception.exceptions import RasError
from requests import HTTPError
from structlog import wrap_logger

log = wrap_logger(logging.getLogger(__name__))


def translate_exceptions(f):
    # TODO: ultimately we don't want to expose error details to the caller, so should possible map expected
    # TODO: errors to something more friendly, and fall back to a generic 500 on unexpected errors
    @wraps(f)
    def wrapper(*args, **kwargs):
        # TODO: log the stack-trace
        try:
            return f(*args, **kwargs)
        except RasError as e:
            log.error(e.to_dict())
            raise
        except HTTPError as e:
            try:
                detail = e.response.json().get('detail', "No further detail")
            except Exception:
                detail = "No further detail"
            raise RasError([str(e), detail])
        except Exception as e:
            log.error(str(e))
            if current_app.config.feature.translate_exceptions:
                raise RasError(str(e))
            else:
                raise
    return wrapper
