import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError

logger = wrap_logger(logging.getLogger(__name__))


def download_collection_exercise_report(collection_exercise_id, survey_id):
    logger.debug('Downloading Collection exercise report', collection_exerise_id=collection_exercise_id, survey_id=survey_id)
    url = f'{app.config["RM_REPORT_SERVICE"]}reporting-api/v1/response-chasing/download-report/{collection_exercise_id}/{survey_id}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])
    if response.status_code != 200:
        logger.error('Error retrieving collection exercise', collection_exercise_id=collection_exercise_id, survey_id=survey_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved collection exercise', collection_exercise_id=collection_exercise_id, survey_id=survey_id)
    return response.content, response.headers.items()
