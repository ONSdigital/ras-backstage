import datetime
from functools import wraps

import requests
from flask import request, current_app
from jose import jwt, JWTError
from ras_common_utils.ras_error.ras_error import RasError
from structlog import get_logger

from ras_backstage.controllers.error_decorator import translate_exceptions

log = get_logger()


PROXY_HEADERS_WHITELIST = [
    'Accept',
    'Authorization'
]


def build_url(service_name, config, proxy_path):
    template = '{}://{}:{}/{}'
    try:
        built_url = template.format(config['scheme'], config['host'], config['port'], proxy_path)
    except KeyError as e:
        raise RasError("Configuration for service '{}' is missing the key {}.".format(service_name, e))
    return built_url


@translate_exceptions
def get_info(config):
    info = {
        "name": config['NAME'],
        "version": config['VERSION'],
    }
    info.update(config.get('METADATA', {}))

    if config.feature.report_dependencies:
        info["dependencies"] = [{'name': name} for name in config.dependency.keys()]

    return info


@translate_exceptions
def sign_in(config, username, password):
    oauth_svc = config.dependency['oauth2-service']
    client_id = oauth_svc['client_id']
    client_secret = oauth_svc['client_secret']

    oauth_payload = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': client_id,
        'client_secret': client_secret
    }

    oauth_url = '{}://{}:{}/api/v1/tokens/'.format(oauth_svc['scheme'], oauth_svc['host'], oauth_svc['port'])
    response = requests.post(oauth_url, auth=(client_id, client_secret), json=oauth_payload)
    response.raise_for_status()

    return response.json()


def validate(token):
    log.debug("Validating JWT token.")

    now = datetime.now().timestamp()
    expires_at = token.get('expires_at')
    if expires_at is None:
        raise RasError("JWT token does not have an expiry time.")
    if now >= expires_at:
        raise RasError("JWT token has expired.")

    log.debug("JWT token is valid")


def jwt_required(request):

    JWT_ALGORITHM = 'HS256'

    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):

            if not current_app.config.feature['validate_jwt']:
                return f(*args, **kwargs)

            oauth_svc = current_app.config.dependency['oauth2-service']
            client_secret = oauth_svc['client_secret']

            try:
                encoded_jwt_token = request.headers['authorization']
            except KeyError:
                raise RasError("No JWT token provided")

            log.debug("Attempting to decode JWT token.")
            try:
                jwt_token = jwt.decode(encoded_jwt_token, client_secret, algorithms=JWT_ALGORITHM)
            except JWTError:
                raise RasError("Failed to decode JWT token.")
            log.debug("JWT token decoded successfully.")

            f(*args, **kwargs, token=jwt_token)
        return decorator
    return wrapper


@translate_exceptions
# @jwt_required(request)
def proxy_request(config, request, service, url):
    try:
        service_config = config.dependency[service]
    except KeyError:
        raise RasError("Service '{}' could not be resolved.".format(service), status_code=404)

    proxy_url = build_url(service, service_config, url)

    # Convert the params to the required format for requests by turning into a dict with list values
    params = request.args.to_dict(flat=False)
    # then turn list values of length 1 into scalars
    params = {k: v[0] if len(v) == 1 else v for k, v in params.items()}

    headers = {k: v for k, v in request.headers.items() if k in PROXY_HEADERS_WHITELIST}

    req = requests.request(method=request.method,
                           url=proxy_url,
                           headers=headers,
                           stream=True,
                           data=request.data,
                           params=params)

    # TODO: consider wrapping exceptions and returning a 502
    # Note: when translated to a json response, this exposes the underlying url we tried to call - is that wanted?
    req.raise_for_status()

    return req
