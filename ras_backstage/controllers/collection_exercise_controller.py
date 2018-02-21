import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_collection_exercise_by_id(collection_exercise_id):
    logger.debug('Retrieving collection exercise', collection_exercise_id=collection_exercise_id)
    url = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}collectionexercises/{collection_exercise_id}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving collection exercise', collection_exercise_id=collection_exercise_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved collection exercise', collection_exercise_id=collection_exercise_id)
    return response.json()


def get_collection_exercises_by_survey(survey_id):
    logger.debug('Retrieving collection exercises', survey_id=survey_id)
    url = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}collectionexercises/survey/{survey_id}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code == 204:
        logger.debug('No collection exercises', survey_id=survey_id)
        return []
    if response.status_code != 200:
        logger.error('Error retrieving collection exercises', survey_id=survey_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved collection exercises', survey_id=survey_id)
    return response.json()


def get_collection_exercises_by_party_id(party_id):
    logger.debug('Retrieving collection exercises', party_id=party_id)
    url = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}collectionexercises/party/{party_id}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code == 204 or response.status_code == 404:
        logger.debug('No collection exercises', party_id=party_id)
        return []
    if response.status_code != 200:
        logger.error('Error retrieving collection exercises', party_id=party_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved collection exercises', party_id=party_id)
    return response.json()


def get_collection_exercise_events(collection_exercise_id):
    logger.debug('Retrieving collection exercise events', collection_exercise_id=collection_exercise_id)
    url = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}collectionexercises/{collection_exercise_id}/events'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving collection exercise events', collection_exercise_id=collection_exercise_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved collection exercise events', collection_exercise_id=collection_exercise_id)
    return response.json()


def get_linked_sample_summary_id(collection_exercise_id):
    logger.debug('Retrieving sample linked to collection exercise', collection_exercise_id=collection_exercise_id)
    url = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}collectionexercises/link/{collection_exercise_id}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code == 204:
        logger.info('No samples linked to collection exercise', collection_exercise_id=collection_exercise_id)
        return
    elif response.status_code != 200:
        logger.error('Error retrieving sample summaries linked to collection exercise',
                     collection_exercise_id=collection_exercise_id)
        raise ApiError(url, response.status_code)

    # currently, we only want a single sample summary
    sample_summary_id = response.json()[0]

    logger.debug('Successfully retrieved linked sample summary',
                 collection_exercise_id=collection_exercise_id,
                 sample_summary_id=sample_summary_id)
    return sample_summary_id


def link_sample_summary_to_collection_exercise(collection_exercise_id, sample_summary_id):
    logger.debug('Linking sample summary to collection exercise',
                 collection_exercise_id=collection_exercise_id,
                 sample_summary_id=sample_summary_id)
    url = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}collectionexercises/link/{collection_exercise_id}'
    # Currently we only need to link a single sample to a single collection exercise
    payload = {'sampleSummaryIds': [str(sample_summary_id)]}
    response = request_handler('PUT', url, auth=app.config['BASIC_AUTH'], json=payload)

    if response.status_code == 404:
        logger.error('Error retrieving collection exercise', collection_exercise_id=collection_exercise_id)
        raise ApiError(url, response.status_code)
    if response.status_code != 200:
        logger.error('Error linking sample to collection exercise',
                     collection_exercise_id=collection_exercise_id,
                     sample_summary_id=sample_summary_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully linked sample summary with collection exercise',
                 collection_exercise_id=collection_exercise_id,
                 sample_summary_id=sample_summary_id)
    return response.json()
