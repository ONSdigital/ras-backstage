from flask import Blueprint, Response, stream_with_context, request, make_response, jsonify, current_app
from ras_common_utils.ras_error.ras_error import RasError
from flask_httpauth import HTTPBasicAuth
from werkzeug.exceptions import BadRequest

from ras_backstage.controllers import controller

backstage_view = Blueprint('backstage_view', __name__)

PROXY_METHODS = ['GET', 'POST', 'PUT', 'DELETE']


auth = HTTPBasicAuth()


@auth.get_password
def get_pw(username):
    config_username = current_app.config['SECURITY_USER_NAME']
    config_password = current_app.config['SECURITY_USER_PASSWORD']
    if username == config_username:
        return config_password


@backstage_view.route('/sign_in', methods=['POST'])
def sign_in():
    errors = []
    try:
        body = request.json
    except BadRequest:
        body = None
    if body is None:
        raise RasError("No JSON supplied in request body.", status_code=400)
    if 'username' not in body:
        errors.append("username is missing from the JSON body.")
    if 'password' not in body:
        errors.append("password is missing from the JSON body.")

    if errors:
        raise RasError(errors, status_code=400)

    username = request.json.get('username')
    password = request.json.get('password')

    resp = controller.sign_in(current_app.config, username, password)
    return make_response(jsonify(resp), 201)


@backstage_view.route('/<string:service>', strict_slashes=False, defaults={'url': ''}, methods=PROXY_METHODS)
@backstage_view.route('/<string:service>/<path:url>', methods=PROXY_METHODS)
def proxy(service, url):
    req = controller.proxy_request(current_app.config, request, service, url)
    return Response(req.content, status=req.status_code, content_type=req.headers['content-type'])
