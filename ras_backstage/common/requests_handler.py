import logging

import requests
from requests.exceptions import RequestException
from structlog import wrap_logger

from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def request_handler(method, url, params=None, auth=None, headers=None, json=None, data=None):
    try:
        if method == 'POST':
            response = requests.post(url, params=params, auth=auth, headers=headers,
                                     json=json, data=data)
        elif method == 'PUT':
            response = requests.put(url, params=params, auth=auth, headers=headers,
                                    json=json, data=data)
        else:
            response = requests.get(url, params=params, auth=auth, headers=headers)
    except RequestException as e:
        logger.exception('Failed to connect to external service',
                         method=method, url=url, exception=str(e))
        raise ApiError(url)

    return response
