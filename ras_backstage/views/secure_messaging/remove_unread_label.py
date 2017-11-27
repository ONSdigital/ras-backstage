import logging

from flask import request
from flask_restplus import reqparse, Resource
from structlog import wrap_logger

from ras_backstage import secure_messaging_api
from ras_backstage.controllers import secure_messaging_controller
from ras_backstage.decorators.jwt_decorators import get_jwt


logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('message_id', location='args', required=True)


@secure_messaging_api.route('/remove-unread')
class RemoveUnreadLabel(Resource):
    method_decorators = [get_jwt(request)]

    @staticmethod
    @secure_messaging_api.expect(parser)
    @secure_messaging_api.header('Authorization', 'JWT to pass to secure messaging service', required=True)
    def put(encoded_jwt):
        message_id = request.args.get('message_id')
        logger.info('Attempting to remove unread message label', message_id=message_id)

        secure_messaging_controller.remove_unread_label(encoded_jwt, message_id)

        logger.info('Successfully removed unread label', message_id=message_id)
        return 200
