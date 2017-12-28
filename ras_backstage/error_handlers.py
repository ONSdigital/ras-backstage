from json import JSONDecodeError
import logging

from flask import jsonify
from structlog import wrap_logger

from ras_backstage import app, api
from ras_backstage.exception.exceptions import ApiError, NoJWTError


logger = wrap_logger(logging.getLogger(__name__))


@app.errorhandler(ApiError)
@api.errorhandler(ApiError)
def api_error_method(error):
    status_code = error.status_code if error.status_code else 500
    error_json = {
        "error": {
            "url": error.url,
            "status_code": status_code,
            "data": error.data
        }
    }
    logger.error('Error during api call', url=error.url, status_code=error.status_code)
    return jsonify(error_json), status_code


@app.errorhandler(JSONDecodeError)
@api.errorhandler(JSONDecodeError)
def json_decode_error(error):
    error_json = {
        "error": {
            "message": error.msg,
            "json": error.doc
        }
    }
    logger.error('Error decoding json object', exc_info=error)
    return jsonify(error_json), 500


@app.errorhandler(NoJWTError)
@api.errorhandler(NoJWTError)
def no_jwt_in_header(error):  # NOQA # pylint: disable=unused-argument
    return {'message': 'No JWT provided in request header'}, 401
