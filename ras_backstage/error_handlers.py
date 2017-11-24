import logging

from flask import jsonify
from structlog import wrap_logger

from ras_backstage import app, api
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


@app.errorhandler(ApiError)
@api.errorhandler(ApiError)
def api_error_method(error):
    error_json = {
        "error": {
            "url": error.url,
            "status_code": error.status_code,
            "data": error.data
        }
    }
    status_code = error.status_code if error.status_code else 500
    logger.error('Error during api call', url=error.url, status_code=error.status_code)
    return jsonify(error_json), status_code
