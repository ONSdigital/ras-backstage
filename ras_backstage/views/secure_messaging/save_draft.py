import logging

from flask import jsonify, make_response, request
from flask_restplus import fields, Resource
from structlog import wrap_logger

from ras_backstage import secure_messaging_api
from ras_backstage.controllers import secure_messaging_controller
from ras_backstage.decorators.jwt_decorators import get_jwt


logger = wrap_logger(logging.getLogger(__name__))


@secure_messaging_api.route('/save-draft')
class SaveDraft(Resource):
    method_decorators = [get_jwt(request)]

    draft_details = secure_messaging_api.model('DraftDetails', {
        'msg_from': fields.String(required=True),
        'subject': fields.String(required=True),
        'body': fields.String(required=True),
        'thread_id': fields.String(),
    })

    @staticmethod
    @secure_messaging_api.expect(draft_details, validate=True)
    @secure_messaging_api.header('Authorization', 'JWT to pass to secure messaging service', required=True)
    def post(encoded_jwt):
        message_json = request.get_json(force=True)
        logger.info('Attempting to save draft')

        message = secure_messaging_controller.save_draft(encoded_jwt, message_json)

        logger.info('Successfully saved draft', message_id=message['msg_id'])
        return make_response(jsonify(message), 201)

    existing_draft_details = secure_messaging_api.model('ExistingDraftDetails', {
        'msg_from': fields.String(required=True),
        'subject': fields.String(required=True),
        'body': fields.String(required=True),
        'msg_id': fields.String(required=True),
        'thread_id': fields.String(),
    })

    @staticmethod
    @secure_messaging_api.expect(existing_draft_details, validate=True)
    @secure_messaging_api.header('Authorization', 'JWT to pass to secure messaging service', required=True)
    def put(encoded_jwt):
        message_json = request.get_json(force=True)
        logger.info('Attempting to update draft')

        message = secure_messaging_controller.update_draft(encoded_jwt, message_json)

        logger.info('Successfully updated draft', message_id=message['msg_id'])
        return make_response(jsonify(message), 200)
