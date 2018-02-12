import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_sample_summary(sample_summary_id):
    logger.debug('Retrieving sample summary', sample_summary_id=sample_summary_id)
    url = f'{app.config["RM_SAMPLE_SERVICE"]}samples/samplesummary/{sample_summary_id}'

    response = request_handler(url=url, method='GET', auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving sample summary',
                     sample_summary_id=sample_summary_id,
                     status_code=response.status_code)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved sample summary', sample_summary_id=sample_summary_id)
    return response.json()


def upload_sample(collection_exercise_id, sample_file, survey_type='B'):
    logger.debug('Uploading sample file',
                 collection_exercise_id=collection_exercise_id,
                 survey_type=survey_type)
    url = f'{app.config["RM_SAMPLE_SERVICE"]}samples/{survey_type}/fileupload'

    response = request_handler(url=url, method='POST', auth=app.config['BASIC_AUTH'], files={'file': sample_file})

    # Sample service *should* return something other than 201 when upload / ingest fails
    if response.status_code != 201:
        logger.error('Error uploading sample file',
                     collection_exercise_id=collection_exercise_id,
                     status=response.status_code,
                     survey_type=survey_type)
        raise ApiError(url, response.status_code)

    response_json = response.json()

    logger.debug('Successfully uploaded sample file',
                 collection_exercise_id=collection_exercise_id,
                 response_json=response_json,
                 survey_type=survey_type)
    return response_json
