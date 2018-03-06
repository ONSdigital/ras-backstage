import logging

from flask import jsonify, make_response, request
from flask_restplus import reqparse, Resource
from structlog import wrap_logger

from ras_backstage import secure_messaging_api
from ras_backstage.controllers import secure_messaging_controller
from ras_backstage.decorators.jwt_decorators import get_jwt


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

        conversation_thread = secure_messaging_controller.get_thread_by_id(encoded_jwt, thread_id)

        # Create json response
        logger.info('Successfully retrieved conversation thread', thread_id=thread_id)
        return make_response(jsonify(conversation_thread), 200)
