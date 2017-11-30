import logging

from flask import jsonify, make_response, request
from flask_restplus import reqparse, Resource
from structlog import wrap_logger

from ras_backstage import secure_messaging_api
from ras_backstage.controllers import secure_messaging_controller
from ras_backstage.decorators.jwt_decorators import get_jwt


logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('label', location='args')
parser.add_argument('limit', location='args')


@secure_messaging_api.route('/messages')
class GetMessagesList(Resource):
    method_decorators = [get_jwt(request)]

    @staticmethod
    @secure_messaging_api.expect(parser)
    @secure_messaging_api.header('Authorization',
                                 'JWT to pass to secure messaging service', required=True)
    def get(encoded_jwt):
        label = request.args.get('label')
        limit = request.args.get('limit')
        logger.info('Attempting to retrieve message list', label=label)

        messages = secure_messaging_controller.get_messages_list(encoded_jwt, label, limit)

        logger.info('Successfully retrieved message list', label=label)
        return make_response(jsonify(messages), 200)
