import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def post_sample_file_for_collection_exercise(collection_exercise_id, filename, sample_file_data, survey_type='bres'):
    url = f'{app.config["RM_SAMPLE_SERVICE"]}{survey_type}/fileupload'
    logger.debug('Uploading sample file',
                 collection_exercise_id=collection_exercise_id,
                 filename=filename,
                 survey_type=survey_type,
                 url=url)

    files_dict = {'file': (filename, sample_file_data, 'text/csv')}
    response = request_handler('POST', url, auth=app.config['BASIC_AUTH'], files=files_dict)

    if response.status_code != 201:
        logger.error('Error uploading sample file',
                     collection_exercise_id=collection_exercise_id,
                     filename=filename,
                     survey_type=survey_type)
        raise ApiError(url, response.status_code)

    sample_id = response.json()['id']

    logger.debug('Successfully uploaded sample file',
                 collection_exercise_id=collection_exercise_id,
                 filename=filename,
                 survey_type=survey_type,
                 sample_id=sample_id)

    return sample_id
