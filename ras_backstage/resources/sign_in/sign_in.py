import logging
import uuid

from flask import current_app, request, make_response, jsonify, abort
from flask_restplus import fields, Resource
from jwt import DecodeError
from structlog import wrap_logger

from ras_backstage import sign_in_api_v2
from ras_backstage.controllers import uaa_controller
from ras_backstage.authentication import token_decoder

logger = wrap_logger(logging.getLogger(__name__))

sign_in_details = sign_in_api_v2.model(
    'SignInDetails', {
        'username': fields.String(required=True, description='username'),
        'password': fields.String(required=True, description='password')
    })


@sign_in_api_v2.route('/', methods=['POST'])
class SignInV2(Resource):
    @staticmethod
    @sign_in_api_v2.expect(sign_in_details, validate=True)
    def post():
        logger.info('Retrieving sign-in details')
        message_json = request.get_json()
        username = message_json.get('username')
        password = message_json.get('password')

        if current_app.config.get('USE_UAA'):
            try:
                logger.info('Retrieving sign-in details')
                access_token = uaa_controller.sign_in(username, password)

                logger.info('Successfully retrieved sign-in details')
                token = token_decoder.decode_access_token(access_token)
                user_id = token.get('user_id')
                return jsonify({"token": access_token, "user_id": user_id})
            except DecodeError:
                logger.error(f"Unable to decode token {access_token} - confirm the UAA public key is correct")
                abort(500)
        else:
            if username == current_app.config['USERNAME'] and password == current_app.config['PASSWORD']:
                logger.info("Authentication successful", user=username)
                return jsonify({"token": uuid.uuid4(), "user_id": username})
            else:
                logger.info("Authentication failed", user=username)
                return make_response(
                    jsonify({
                        "error": "Username and/or password incorrect"
                    }), 401)
