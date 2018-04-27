import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.filters import get_collection_exercise_by_period
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.controllers import survey_controller
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


def get_collection_exercise_and_survey(short_name, period):
    survey = survey_controller.get_survey_by_shortname(short_name)
    exercises = get_collection_exercises_by_survey(survey['id'])
    exercise = get_collection_exercise_by_period(exercises, period)
    return {
        "collection_exercise": exercise,
        "survey": survey
    }


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


def update_event(collection_exercise_id, tag, timestamp):
    logger.debug('Updating event',
                 collection_exercise_id=collection_exercise_id, tag=tag)
    url = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}collectionexercises/{collection_exercise_id}/events/{tag}'
    response = request_handler('PUT', url, auth=app.config['BASIC_AUTH'],
                               headers={'content-type': 'text/plain'}, data=timestamp)

    if not response.ok:
        logger.error('Error updating event',
                     collection_exercise_id=collection_exercise_id, tag=tag)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully updated event',
                 collection_exercise_id=collection_exercise_id, tag=tag)


def create_event(collection_exercise_id, tag, event_dto):
    logger.debug('Creating event', collection_exercise_id=collection_exercise_id, tag=tag)
    url = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}collectionexercises/{collection_exercise_id}/events'
    response = request_handler('POST', url, auth=app.config['BASIC_AUTH'], json=event_dto)

    if not response.ok:
        logger.error('Error creating event',
                     collection_exercise_id=collection_exercise_id, tag=tag)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully created event',
                 collection_exercise_id=collection_exercise_id, tag=tag)


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


def execute_collection_exercise(collection_exercise_id):
    logger.debug('Executing collection exercise', collection_exercise_id=collection_exercise_id)
    url = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}collectionexerciseexecution/{collection_exercise_id}'
    response = request_handler('POST', url, auth=app.config['BASIC_AUTH'])

    if response.status_code == 404:
        logger.error('Error retrieving collection exercise', collection_exercise_id=collection_exercise_id)
        raise ApiError(url, response.status_code)
    if response.status_code not in (200, 201, 202):
        logger.error('Error executing collection exercise', collection_exercise_id=collection_exercise_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully executed collection exercise', collection_exercise_id=collection_exercise_id)


def update_collection_exercise_user_description(collection_exercise_id, user_description):
    logger.debug('Updating collection exercise user description', collection_exercise_id=collection_exercise_id,
                 user_description=user_description)
    header = {'Content-Type': "text/plain"}
    url = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}collectionexercises/{collection_exercise_id}/userDescription'
    response = request_handler('PUT', url, headers=header, data=user_description, auth=app.config['BASIC_AUTH'])

    if response.status_code == 404:
        logger.error('Error retrieving collection exercise', collection_exercise_id=collection_exercise_id)
        raise ApiError(url, response.status_code)
    if response.status_code not in (200, 201, 202):
        logger.error('Error updating collection exercise user description',
                     collection_exercise_id=collection_exercise_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully updated collection exercise user description',
                 collection_exercise_id=collection_exercise_id)


def update_collection_exercise_period(collection_exercise_id, period):
    logger.debug('Updating collection exercise period', collection_exercise_id=collection_exercise_id,
                 period=period)
    header = {'Content-Type': "text/plain"}
    url = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}collectionexercises/{collection_exercise_id}/exerciseRef'
    response = request_handler('PUT', url, headers=header, data=period, auth=app.config['BASIC_AUTH'])

    if response.status_code == 404:
        logger.error('Error retrieving collection exercise', collection_exercise_id=collection_exercise_id)
        raise ApiError(url, response.status_code)
    if response.status_code not in (200, 201, 202):
        logger.error('Error updating collection exercise period', collection_exercise_id=collection_exercise_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully updated collection exercise period', collection_exercise_id=collection_exercise_id)


def create_collection_exercise(created_collection_exercise_details):
    logger.debug('Creating new collection exercise')
    header = {'Content-Type': "application/json"}
    url = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}collectionexercises'

    payload = {
        "surveyId": created_collection_exercise_details['survey_id'],
        "name": created_collection_exercise_details['survey_name'],
        "userDescription": created_collection_exercise_details['user_description'],
        "exerciseRef": created_collection_exercise_details['period']
    }

    response = request_handler('POST', url, json=payload, headers=header, auth=app.config['BASIC_AUTH'])

    if response.status_code == 404:
        logger.error('Error retrieving new collection exercise data')
        raise ApiError(url, response.status_code)
    if response.status_code not in (200, 201, 202):
        logger.error('Error creating new collection exercise')
        raise ApiError(url, response.status_code)

    logger.debug('Successfully created a new collection exercise')
