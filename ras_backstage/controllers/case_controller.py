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


def get_available_statuses_for_ru_ref(collection_exercise_id, ru_ref):
    logger.debug('Retrieving statuses', collection_exercise_id=collection_exercise_id, ru_ref=ru_ref)
    url = f'{app.config["RM_CASE_SERVICE"]}casegroups/transitions/{collection_exercise_id}/{ru_ref}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving statuses', collection_exercise_id=collection_exercise_id, ru_ref=ru_ref)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved statuses', collection_exercise_id=collection_exercise_id, ru_ref=ru_ref)
    return response.json()


def update_case_group_status(collection_exercise_id, ru_ref, case_group_event):
    logger.debug('Updating status', collection_exercise_id=collection_exercise_id, ru_ref=ru_ref, case_group_event=case_group_event)
    url = f'{app.config["RM_CASE_SERVICE"]}casegroups/transitions/{collection_exercise_id}/{ru_ref}'
    response = request_handler('PUT', url, auth=app.config['BASIC_AUTH'], json={'event': case_group_event})

    if response.status_code != 200:
        logger.error('Error updating status', collection_exercise_id=collection_exercise_id,ru_ref=ru_ref,
                     case_group_event=case_group_event)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully updated status', collection_exercise_id=collection_exercise_id, ru_ref=ru_ref,
                 case_group_event=case_group_event)
