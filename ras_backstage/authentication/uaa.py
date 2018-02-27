import logging

import requests
from requests import HTTPError
from json import JSONDecodeError
from flask import current_app

logger = logging.getLogger(__name__)


def request_uaa_public_key(app):
    headers = {
        'Accept': 'application/json',
    }

    public_key_url = f'{app.config["UAA_SERVICE_URL"]}{"/token_key"}'
    response = requests.get(public_key_url, headers=headers)

    try:
        response.raise_for_status()
        key = response.json()['value']
        return key
    except KeyError:
        logger.exception("No public key returned by UAA")
    except (JSONDecodeError, ValueError):
        logger.exception("Unexpected returned by UAA")
    except HTTPError:
        logger.exception("Error while retrieving public key from UAA")
    return None


def get_uaa_public_key():
    if not current_app.config.get('UAA_PUBLIC_KEY'):
        current_app.config['UAA_PUBLIC_KEY'] = request_uaa_public_key(current_app)

    return current_app.config['UAA_PUBLIC_KEY']
