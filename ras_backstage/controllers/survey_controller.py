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


def get_survey_ci_classifier(survey_id):
    logger.debug('Retrieving classifier type selectors', survey_id=survey_id)
    url = f'{app.config["RM_SURVEY_SERVICE"]}surveys/{survey_id}/classifiertypeselectors'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error classifier type selectors', survey_id=survey_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved classifier type selectors', survey_id=survey_id)

    classifier_type_selectors = response.json()
    ci_selector = None
    for selector in classifier_type_selectors:
        if selector['name'] == "COLLECTION_INSTRUMENT":
            ci_selector = selector
            break

    logger.debug('Retrieving classifiers for CI selector type', survey_id=survey_id, ci_selector=ci_selector['id'])
    url = f'{app.config["RM_SURVEY_SERVICE"]}surveys/{survey_id}/classifiertypeselectors/{ci_selector["id"]}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving classifiers for CI selector type', survey_id=survey_id,
                     ci_selector=ci_selector['id'])
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved classifiers for CI selector type', survey_id=survey_id,
                 ci_selector=ci_selector['id'])

    return response.json()


def update_survey_details(survey_ref, updated_survey_details):
    logger.debug('Updating survey details', survey_ref=survey_ref)
    url = f'{app.config["RM_SURVEY_SERVICE"]}surveys/ref/{survey_ref}'
    payload = {
        "ShortName": updated_survey_details['short_name'],
        "LongName": updated_survey_details['long_name']
    }

    response = request_handler('PUT', url, auth=app.config['BASIC_AUTH'], json=payload)

    if response.status_code == 404:
        logger.error('Error retrieving survey details', survey_ref=survey_ref)
        raise ApiError(url, response.status_code)
    if not response.ok:
        logger.error('Error updating survey details', survey_ref=survey_ref)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully updated survey details', survey_ref=survey_ref)
