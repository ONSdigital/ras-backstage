from datetime import datetime, timedelta
import logging

from flask import request, make_response, jsonify
from flask_restplus import fields, Resource
from jose import jwt
from structlog import wrap_logger

from ras_backstage import app, sign_in_uaa_api


logger = wrap_logger(logging.getLogger(__name__))

sign_in_details = sign_in_uaa_api.model('SignInDetails', {
        'username': fields.String(required=True, description='username'),
        'password': fields.String(required=True, description='password')
})


@sign_in_uaa_api.route('/', methods=['POST'])
class SignInUaa(Resource):

    @staticmethod
    @sign_in_uaa_api.expect(sign_in_details, validate=True)
    def post():
        logger.info('Retrieving sign-in details')
        message_json = request.get_json(force=True)
        username = message_json['username']
        password = message_json['password']
        logger.info("json", json=message_json)
        logger.info("username", user=username)
        logger.info("password", blah=password)

        # Obviously horrible, stopgap until uaa is implemented
        if username == 'user' and password == 'pass':
            return make_response(jsonify({"token": "1234abc"}), 200)
        else:
            return make_response(jsonify({"error": "Username and/or password incorrect"}), 401)
