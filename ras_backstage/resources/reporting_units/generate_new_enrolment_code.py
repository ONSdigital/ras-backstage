import logging

from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import reporting_unit_api
from ras_backstage.controllers import case_controller

logger = wrap_logger(logging.getLogger(__name__))


@reporting_unit_api.route('/iac/<collection_exercise_id>/<ru_ref>')
class GenerateNewEnrolmentCode(Resource):

    @staticmethod
    def post(collection_exercise_id, ru_ref):
        logger.info('Generating new enrolment code', collection_exercise_id=collection_exercise_id, ru_ref=ru_ref)
        case = case_controller.generate_new_enrolment_code(collection_exercise_id, ru_ref)
        logger.info('Successfully generated new enrolment code', collection_exercise_id=collection_exercise_id, ru_ref=ru_ref)
        return case
