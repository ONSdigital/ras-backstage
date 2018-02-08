import logging

import jwt
import requests
import pprint


from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_public_key():
    # TODO this needs to be done at start up
    headers = {
        'Accept': 'application/json'
    }

    public_key_url = '{}{}'.format(app.config['UAA_SERVICE_URL'], '/token_key')
    response = requests.get(public_key_url, headers=headers)

    if response.status_code == 200:
        key = response.json().get('value')
        print(key)
        return key
    else:
        raise ApiError(public_key_url, response.status_code)


def sign_in(username, password):
    #  this doesn't work, don't think the UAA is configured correctly
    logger.debug('Retrieving OAuth2 token for sign-in')
    url = '{}{}'.format(app.config['UAA_SERVICE_URL'], '/oauth/token')
    print(url)

    data = {
        'grant_type': 'password',
        'client_id': app.config['UAA_CLIENT_ID'],
        'client_secret': app.config['UAA_CLIENT_SECRET'],
        'username': username,
        'password': password,
        'response_type': 'token_id',
        'token_format': 'jwt'
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }
    response = request_handler('POST', url, data=data, headers=headers)

    if response.status_code != 200:
        logger.error(f'Failed to retrieve OAuth2 token {response.text}')
        raise ApiError(url, response.status_code)

    resp_json = response.json()
    pprint.pprint(resp_json)

    # verify the token
    decoded_jwt = jwt.decode(resp_json.get("access_token"),
                             algorithms=resp_json.get('alg'),
                             verify=True,
                             key=get_public_key(),
                             audience='ras_backstage',
                             leeway=10)
    pprint.pprint(decoded_jwt)

    logger.debug('Successfully retrieved UAA token')
    return decoded_jwt
