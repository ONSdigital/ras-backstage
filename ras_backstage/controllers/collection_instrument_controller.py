import json
import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError

logger = wrap_logger(logging.getLogger(__name__))


def upload_collection_instrument(survey_id, collection_exercise_id, file):
    logger.debug('Uploading collection instrument', collection_exercise_id=collection_exercise_id, survey_id=survey_id)
    url = f'{app.config["RAS_COLLECTION_INSTRUMENT_SERVICE"]}' \
          f'collection-instrument-api/1.0.2/upload/{collection_exercise_id}'

    classifiers = {}
    if survey_id:
        classifiers['SURVEY_ID'] = survey_id
    if collection_exercise_id:
        classifiers['COLLECTION_EXERCISE'] = collection_exercise_id

    request_handler(url=url, method='POST', auth=app.config['BASIC_AUTH'], files={'file': file},
                    params={'classifiers': json.dumps(classifiers)})

    logger.debug('Successfully uploaded collection instrument',
                 collection_exercise_id=collection_exercise_id)


def get_collection_instruments_by_classifier(survey_id, collection_exercise_id):
    logger.debug('Retrieving collection instruments', survey_id=survey_id,
                 collection_exercise_id=collection_exercise_id)
    url = f'{app.config["RAS_COLLECTION_INSTRUMENT_SERVICE"]}' \
          f'collection-instrument-api/1.0.2/collectioninstrument'

    classifiers = {}
    if survey_id:
        classifiers['SURVEY_ID'] = survey_id
    if collection_exercise_id:
        classifiers['COLLECTION_EXERCISE'] = collection_exercise_id

    response = request_handler(url=url, method='GET', auth=app.config['BASIC_AUTH'],
                               params={'searchString': json.dumps(classifiers)})

    if response.status_code != 200:
        logger.error('Error retrieving collection instruments')
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved collection instruments', survey_id=survey_id,
                 collection_exercise_id=collection_exercise_id)
    return json.loads(response.text)
