import json
import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_party_by_business_id(party_id):
    logger.debug('Retrieving business party', party_id=party_id)
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/businesses/id/{party_id}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving business party', party_id=party_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved business party', party_id=party_id)
    return json.loads(response.text)


def get_party_by_respondent_id(party_id):
    logger.debug('Retrieving respondent party', party_id=party_id)
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/respondents/id/{party_id}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving respondent party', party_id=party_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved respondent party', party_id=party_id)
    return json.loads(response.text)


def get_businesses_by_search(query):
    logger.debug('Retrieving businesses by search query', query=query)
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/businesses/search'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'], params={"query": query})

    if response.status_code != 200:
        logger.error('Error retrieving businesses by search query', query=query)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved businesses by search query')
    return json.loads(response.text)
