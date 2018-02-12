import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_survey_list():
    logger.debug('Retrieving survey list')
    url = f'{app.config["RM_SURVEY_SERVICE"]}surveys'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code == 204:
        logger.debug('No surveys found in survey service')
        return []
    if response.status_code != 200:
        logger.error('Error retrieving the survey list')
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved the survey list')
    return response.json()


def get_survey_by_id(survey_id):
    logger.debug('Retrieving survey', survey_id=survey_id)
    url = f'{app.config["RM_SURVEY_SERVICE"]}surveys/{survey_id}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving survey', survey_id=survey_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved survey', survey_id=survey_id)
    return response.json()


def get_survey_by_shortname(short_name):
    logger.debug('Retrieving survey', short_name=short_name)
    url = f'{app.config["RM_SURVEY_SERVICE"]}surveys/shortname/{short_name}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving survey', short_name=short_name)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved survey', short_name=short_name)
    return response.json()
