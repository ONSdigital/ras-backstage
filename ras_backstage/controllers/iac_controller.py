import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_iac(iac_code):
    logger.debug('Retrieving iac', iac_code=iac_code)
    url = f'{app.config["RM_IAC_SERVICE"]}iacs/{iac_code}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving iac', iac_code=iac_code)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved iac', iac_code=iac_code)
    return response.json()
