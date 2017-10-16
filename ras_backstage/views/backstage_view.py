import logging
from werkzeug.exceptions import BadRequest

from flask import Blueprint, Response, request, make_response, jsonify, current_app
from flask_httpauth import HTTPBasicAuth
from structlog import wrap_logger

from ras_backstage.exception.exceptions import RasError
from ras_backstage.controllers import controller

backstage_view = Blueprint('backstage_view', __name__)

PROXY_METHODS = ['GET', 'POST', 'PUT', 'DELETE']

logger = wrap_logger(logging.getLogger(__name__))

auth = HTTPBasicAuth()


@auth.get_password
def get_pw(username):
    config_username = current_app.config['SECURITY_USER_NAME']
    config_password = current_app.config['SECURITY_USER_PASSWORD']
    if username == config_username:
        return config_password


@backstage_view.route('/sign_in', methods=['POST'])
def sign_in():
    logger.info("Sign-in POST request.")

    errors = []
    try:
        body = request.get_json(force=True)
    except BadRequest:
        raise RasError("No JSON supplied in request body.", status_code=400)

    if 'username' not in body:
        errors.append("username is missing from the JSON body.")
    if 'password' not in body:
        errors.append("password is missing from the JSON body.")

    if errors:
        raise RasError(errors, status_code=400)

    username = body.get('username')
    password = body.get('password')

    resp = controller.sign_in(current_app.config, username, password)
    return make_response(jsonify(resp), 201)


@backstage_view.route('/<string:service>', strict_slashes=False, defaults={'url': ''}, methods=PROXY_METHODS)
@backstage_view.route('/<string:service>/<path:url>', methods=PROXY_METHODS)
def proxy(service, url):
    req = controller.proxy_request(current_app.config, request, service, url)
    return Response(req.content, status=req.status_code, content_type=req.headers['content-type'])
