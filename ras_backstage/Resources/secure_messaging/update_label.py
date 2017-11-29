import logging

from flask import request
from flask_restplus import fields, Resource
from structlog import wrap_logger

from ras_backstage import secure_messaging_api
from ras_backstage.controllers import secure_messaging_controller
from ras_backstage.decorators.jwt_decorators import get_jwt


logger = wrap_logger(logging.getLogger(__name__))

label_details = secure_messaging_api.model('LabelDetails', {
        'label': fields.String(required=True),
        'action': fields.String(required=True),
})


@secure_messaging_api.route('/update-label/<message_id>')
class RemoveUnreadLabel(Resource):
    method_decorators = [get_jwt(request)]

    @staticmethod
    @secure_messaging_api.expect(label_details)
    @secure_messaging_api.header('Authorization', 'JWT to pass to secure messaging service', required=True)
    def put(encoded_jwt, message_id):
        message_json = request.get_json(force=True)
        label = message_json.get('label')
        action = message_json.get('action')
        logger.info('Attempting to update label', message_id=message_id, label=label, action=action)

        secure_messaging_controller.update_label(encoded_jwt, message_id, label, action)

        logger.info('Successfully updated label', message_id=message_id, label=label, action=action)
        return 200
