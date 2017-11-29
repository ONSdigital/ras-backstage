import logging

from flask import jsonify, make_response, request
from flask_restplus import Resource, reqparse
from structlog import wrap_logger

from ras_backstage import secure_messaging_api
from ras_backstage.controllers import secure_messaging_controller
from ras_backstage.decorators.jwt_decorators import get_jwt


logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('message_id', location='args', required=True)
parser.add_argument('is_draft', location='args', required=True)


@secure_messaging_api.route('/message')
class GetMessage(Resource):
    method_decorators = [get_jwt(request)]

    @staticmethod
    @secure_messaging_api.expect(parser)
    @secure_messaging_api.header('Authorization', 'JWT to pass to secure messaging service', required=True)
    def get(encoded_jwt):
        message_id = request.args.get('message_id')
        is_draft = request.args.get('is_draft')
        logger.info('Attempting to retrieve message', message_id=message_id, is_draft=is_draft)

        message = secure_messaging_controller.get_message(encoded_jwt, message_id, is_draft)

        # Create json response
        logger.info('Successfully retrieved message', message_id=message_id, is_draft=is_draft)
        return make_response(jsonify(message), 200)
