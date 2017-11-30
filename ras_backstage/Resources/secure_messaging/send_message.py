import logging

from flask import jsonify, make_response, request
from flask_restplus import fields, Resource
from structlog import wrap_logger

from ras_backstage import secure_messaging_api
from ras_backstage.controllers import secure_messaging_controller
from ras_backstage.decorators.jwt_decorators import get_jwt


logger = wrap_logger(logging.getLogger(__name__))

message_details = secure_messaging_api.model('MessageDetails', {
        'msg_from': fields.String(required=True),
        'subject': fields.String(required=True),
        'body': fields.String(required=True),
        'thread_id': fields.String(),
})


@secure_messaging_api.route('/send-message')
class SendMessage(Resource):
    method_decorators = [get_jwt(request)]

    @staticmethod
    @secure_messaging_api.expect(message_details, validate=True)
    @secure_messaging_api.header('Authorization',
                                 'JWT to pass to secure messaging service', required=True)
    def post(encoded_jwt):
        message_json = request.get_json(force=True)
        logger.info('Attempting to send message')

        message = secure_messaging_controller.send_message(encoded_jwt, message_json)

        logger.info('Successfully sent message', message_id=message['msg_id'])
        return make_response(jsonify(message), 201)
