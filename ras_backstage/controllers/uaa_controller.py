import json
import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def sign_in(username, password):
    logger.debug('Retrieving OAuth2 token for sign-in')
    url = f"{app.config['UAA_SERVICE_URL']}/oauth/token",

    data = {
        'grant_type': 'password',
        'client_id': app.config['UAA_CLIENT_ID'],
        'client_secret': app.config['UAA_CLIENT_SECRET'],
        'username': username,
        'password': password,
        'response_type': 'token',
        'token_format': 'opaque'
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }
    response = request_handler('POST', url, data=data, headers=headers)

    if response.status_code != 200:
        logger.error(f'Failed to retrieve OAuth2 token {response.text}')
        raise ApiError(url, response.status_code)

    oauth2_token = json.loads(response.text)
    logger.debug('Successfully retrieved OAuth2 token')
    return oauth2_token
