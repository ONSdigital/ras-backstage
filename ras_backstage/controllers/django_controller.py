import json
import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def sign_in(username, password):
    logger.debug('Retrieving OAuth2 token for sign-in')
    url = f"{app.config['RAS_OAUTH_SERVICE']}api/v1/tokens/"
    data = {
        'grant_type': 'password',
        'client_id': app.config['DJANGO_CLIENT_ID'],
        'client_secret': app.config['DJANGO_CLIENT_SECRET'],
        'username': username,
        'password': password,
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }
    response = request_handler('POST', url, data=data,
                               headers=headers, auth=app.config['DJANGO_BASIC_AUTH'])

    if response.status_code != 201:
        logger.error('Failed to retrieve OAuth2 token')
        raise ApiError(url, response.status_code)

    oauth2_token = json.loads(response.text)
    logger.debug('Successfully retrieved OAuth2 token')
    return oauth2_token
