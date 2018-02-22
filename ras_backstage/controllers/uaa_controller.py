import logging

import pprint
import jwt
import requests
from requests import HTTPError
from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError

logger = wrap_logger(logging.getLogger(__name__))


def sign_in(username, password):
    logger.debug('Retrieving OAuth2 token for sign-in')
    url = f'{app.config["UAA_SERVICE_URL"]}{"/oauth/token"}'

    data = {
        'grant_type': 'password',
        'client_id': app.config['UAA_CLIENT_ID'],
        'client_secret': app.config['UAA_CLIENT_SECRET'],
        'username': username,
        'password': password,
        'response_type': 'token',
        'token_format': 'jwt',
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }

    response = request_handler('POST', url, data=data, headers=headers)

    try:
        response.raise_for_status()
    except HTTPError:
        logger.exception(f'Failed to retrieve OAuth2 token {response.text}')
        raise ApiError(url, response.status_code)

    try:
        pprint.pprint(response.json())

        logger.debug('Successfully retrieved UAA token')
        token = response.json()

        access_token = token.get('access_token')
        return access_token
    except KeyError:
        logger.exception("No access_token claim in jwt")
        raise ApiError(url, status_code=401)
