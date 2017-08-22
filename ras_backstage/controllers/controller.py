import datetime
from functools import wraps

import requests
from flask import request, current_app
from jose import jwt, JWTError
from ras_common_utils.ras_error.ras_error import RasError
from structlog import get_logger

from ras_backstage.controllers.error_decorator import translate_exceptions

log = get_logger()


JWT_ALGORITHM = 'HS256'
PROXY_HEADERS_WHITELIST = [
    'Accept',
    'Authorization',
    'Content-Type'
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
        'password': password
    }

    oauth_url = '{}://{}:{}/api/v1/tokens/'.format(oauth_svc['scheme'], oauth_svc['host'], oauth_svc['port'])
    payload = '&'.join(["{}={}".format(k, v) for k, v in oauth_payload.items()])
    response = requests.post(oauth_url,
                             auth=(client_id, client_secret),
                             data=payload,
                             headers={'Content-Type': "application/x-www-form-urlencoded"})
    response.raise_for_status()
    response_data = response.json()

    token_expiry = datetime.datetime.now() + datetime.timedelta(seconds=int(response_data['expires_in']))
    response_data['expires_at'] = token_expiry.timestamp()
    # FIXME: remove hard-coded values
    response_data['party_id'] = 'BRES'
    response_data['role'] = 'internal'

    token = jwt.encode(response_data, client_secret, algorithm=JWT_ALGORITHM)

    return {'token': token}


def validate_jwt(client_secret, encoded_jwt_token):
    log.debug("Attempting to validate JWT token.")
    try:
        jwt_token = jwt.decode(encoded_jwt_token, client_secret, algorithms=JWT_ALGORITHM)
    except JWTError:
        raise RasError("Failed to decode JWT token.", status_code=401)

    now = datetime.datetime.now()
    expires_at = datetime.datetime.fromtimestamp(jwt_token['expires_at'])

    if now > expires_at:
        raise RasError("Token has expired.", status_code=401)

    log.debug("JWT token validated successfully.")
    return jwt_token


def jwt_required(request):
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
                raise RasError("No JWT token provided", status_code=401)

            jwt_token = validate_jwt(client_secret, encoded_jwt_token)
            f(*args, **kwargs, token=jwt_token)
        return decorator
    return wrapper


@translate_exceptions
@jwt_required(request)
def proxy_request(config, request, service, url, token=None):
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

    # TODO: do we pass through the incoming Authorization header?
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
