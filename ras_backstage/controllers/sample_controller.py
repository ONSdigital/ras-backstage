import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def upload_sample(survey_id, collection_exercise_id, sample_file, survey_type='B'):
    logger.debug('Uploading sample file',
                 collection_exercise_id=collection_exercise_id,
                 survey_id=survey_id,
                 survey_type=survey_type)
    url = f'{app.config["RM_SAMPLE_SERVICE"]}samples/{survey_type}/fileupload'

    response = request_handler(url=url, method='POST', auth=app.config['BASIC_AUTH'], files={'file': sample_file})

    if response.status_code != 201:
        logger.error('Error uploading sample file',
                     collection_exercise_id=collection_exercise_id,
                     survey_id=survey_id,
                     survey_type=survey_type)
        raise ApiError(url, response.status_code)

    response_json = response.json()

    logger.debug('Successfully uploaded sample file',
                 collection_exercise_id=collection_exercise_id,
                 response_json=response_json,
                 survey_id=survey_id,
                 survey_type=survey_type)

    return response_json