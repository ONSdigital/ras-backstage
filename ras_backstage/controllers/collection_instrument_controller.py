import json
import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler

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

    files = {"file": (file.filename, file.stream, file.mimetype)}
    request_handler(url=url, method='POST', auth=app.config['BASIC_AUTH'], files=files,
                    params={'classifiers': json.dumps(classifiers)})

    logger.debug('Successfully uploaded collection instrument',
                 collection_exercise_id=collection_exercise_id)
