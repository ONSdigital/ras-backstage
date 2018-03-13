import json
import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_party_by_business_id(party_id, collection_exercise_id=None):
    logger.debug('Retrieving business party', party_id=party_id)
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/businesses/id/{party_id}'
    params = {"collection_exercise_id": collection_exercise_id, "verbose": True}
    response = request_handler('GET', url, params=params, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving business party', party_id=party_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved business party', party_id=party_id)
    return response.json()


def get_party_by_respondent_id(party_id):
    logger.debug('Retrieving respondent party', party_id=party_id)
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/respondents/id/{party_id}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving respondent party', party_id=party_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved respondent party', party_id=party_id)
    return response.json()


def get_party_by_ru_ref(ru_ref):
    logger.debug('Retrieving reporting unit', ru_ref=ru_ref)
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/parties/type/B/ref/{ru_ref}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving reporting unit', ru_ref=ru_ref)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved reporting unit', ru_ref=ru_ref)
    return response.json()


def get_businesses_by_search(query):
    logger.debug('Retrieving businesses by search query', query=query)
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/businesses/search'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'], params={"query": query})

    if response.status_code != 200:
        logger.error('Error retrieving businesses by search query', query=query)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved businesses by search query')
    return json.loads(response.text)


def update_respondent_details(respondent_id, first_name, last_name, telephone):
    logger.debug('Updating respondent details', respondent_id=respondent_id)
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/respondents/id/{respondent_id}'
    payload = {
        "firstName": first_name,
        "lastName": last_name,
        "telephone": telephone
        }

    response = request_handler('PUT', url, json=payload, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error updating respondent details', respondent_id=respondent_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully updated respondent details')


def resend_verification_email(party_id):
    logger.debug('Resending verification email', party_id=party_id)
    url = app.config['RAS_PARTY_RESEND_VERIFICATION_EMAIL'].format(party_id)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Failed to resend verification email', party_id=party_id)
        raise ApiError(url=url, status_code=response.status_code)

    logger.debug('Successfully resent verification email')
