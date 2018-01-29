import logging

from flask import request, make_response, jsonify
from flask_restplus import fields, Resource
from structlog import wrap_logger

from ras_backstage import sign_in_uaa_api


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
        # force=true means the post doesn't HAVE to have application/json
        # in its content type.  This feels wrong to me but is also in the django signin code...
        message_json = request.get_json(force=True)
        username = message_json.get('username')
        password = message_json.get('password')

        # Obviously horrible, stopgap until uaa is implemented
        if username == 'user' and password == 'pass':
            # We're assuming that uaa will return an Oauth2 token though it's almost certain that
            # this will change once we know exactly what is being returned.
            logger.info("Authentication successful", user=username)
            return make_response(jsonify({"token": "1234abc"}), 201)
        else:
            logger.info("Authentication failed", user=username)
            return make_response(jsonify({"error": "Username and/or password incorrect"}), 401)
