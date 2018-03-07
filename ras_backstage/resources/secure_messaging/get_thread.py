import logging
from json import JSONDecodeError

from flask import jsonify, make_response, request
from flask_restplus import reqparse, Resource
from structlog import wrap_logger

from ras_backstage import secure_messaging_api
from ras_backstage.controllers import secure_messaging_controller
from ras_backstage.decorators.jwt_decorators import get_jwt
from ras_backstage.exception.exceptions import ApiError

logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()


@secure_messaging_api.route('/threads/<thread_id>')
class GetThread(Resource):
    method_decorators = [get_jwt(request)]

    @staticmethod
    @secure_messaging_api.expect(parser)
    @secure_messaging_api.header('Authorization',
                                 'JWT to pass to secure messaging service', required=True)
    def get(encoded_jwt, thread_id):

        try:
            return make_response(jsonify(secure_messaging_controller.get_thread_by_id(encoded_jwt, thread_id)), 200)
        except ApiError:
            err_msg = f"Failed to retrieve Thread data with thread id: {thread_id}"

        except JSONDecodeError:
            err_msg = f"Secure message returned a malformed Json for id: {thread_id}"

        logger.error(err_msg)

        return make_response(jsonify({'error': err_msg}), 500)
