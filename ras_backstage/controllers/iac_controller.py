import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_iac(iac):
    logger.debug('Retrieving iac')
    url = f'{app.config["RM_IAC_SERVICE"]}iacs/{iac}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code == 404:
        logger.warning('IAC code not found')
        return
    if response.status_code != 200:
        logger.error('Error retrieving iac')
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved iac')
    return response.json()
