from datetime import datetime, timedelta
import logging

from flask import request, make_response, jsonify
from flask_restplus import fields, Resource
from jose import jwt
from structlog import wrap_logger

from ras_backstage import app, sign_in_api
from ras_backstage.controllers import django_controller


logger = wrap_logger(logging.getLogger(__name__))

sign_in_details = sign_in_api.model('SignInDetails', {
        'username': fields.String(required=True, description='username'),
        'password': fields.String(required=True, description='password')
})


@sign_in_api.route('/', methods=['POST'])
class SignIn(Resource):

    @staticmethod
    @sign_in_api.expect(sign_in_details, validate=True)
    def post():
        logger.info('Attempting to retrieved sign-in details')
        message_json = request.get_json(force=True)
        username = message_json['username']
        password = message_json['password']

        oauth2_token = django_controller.sign_in(username, password)
        token_expiry = datetime.now() + timedelta(seconds=int(oauth2_token['expires_in']))
        oauth2_token['expires_at'] = token_expiry.timestamp()
        oauth2_token['party_id'] = 'BRES'
        oauth2_token['role'] = 'internal'

        jwt_secret = app.config['JWT_SECRET']
        token = jwt.encode(oauth2_token, jwt_secret, algorithm=app.config['JWT_ALGORITHM'])

        logger.info('Successfully retrieved sign-in details')
        return make_response(jsonify({"token": token}), 201)
