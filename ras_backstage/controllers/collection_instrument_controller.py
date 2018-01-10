import logging

import requests
from requests import RequestException
from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.exception.exceptions import ApiError

logger = wrap_logger(logging.getLogger(__name__))


def upload_collection_instrument(survey_id, collection_exercise_id, file):
    logger.debug('Uploading collection instrument', collection_exercise_id=collection_exercise_id)
    url = f'{app.config["RAS_COLLECTION_INSTRUMENT_SERVICE"]}upload/{collection_exercise_id}'

    classifiers = {}
    if survey_id:
        classifiers['SURVEY_ID'] = survey_id
    if collection_exercise_id:
        classifiers['COLLECTION_EXERCISE'] = collection_exercise_id
    try:
        response = requests.post(url, auth=app.config['BASIC_AUTH'], files={'file': file})

        if response.status_code != 200:
            logger.error('Error retrieving collection exercise',
                         collection_exercise_id=collection_exercise_id)
            raise ApiError(url, response.status_code)

        logger.debug('Successfully uploaded collection instrument',
                     collection_exercise_id=collection_exercise_id)
    except RequestException as e:
        logger.exception('Failed to connect to external service', method='POST', url=url)
        raise ApiError(url)
