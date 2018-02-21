import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_cases_by_business_party_id(business_party_id):
    logger.debug('Retrieving cases', business_party_id=business_party_id)
    url = f'{app.config["RM_CASE_SERVICE"]}cases/partyid/{business_party_id}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'], params={"iac": "True"})

    if response.status_code == 404 or response.status_code == 204:
        logger.debug('No cases found for business', business_party_id=business_party_id)
        return []
    if response.status_code != 200:
        logger.error('Error retrieving cases', business_party_id=business_party_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved cases', business_party_id=business_party_id)
    return response.json()
