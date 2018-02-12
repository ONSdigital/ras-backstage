import logging

from flask import jsonify, make_response
from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import reporting_unit_api
from ras_backstage.common.filters import get_case_group_status_by_collection_exercise
from ras_backstage.controllers import case_controller, collection_exercise_controller, party_controller, survey_controller


logger = wrap_logger(logging.getLogger(__name__))


@reporting_unit_api.route('/<ru_ref>')
class GetReportingUnit(Resource):

    @staticmethod
    def get(ru_ref):
        logger.info('Retrieving reporting unit details', ru_ref=ru_ref)
        # Retrieve reporting unit
        reporting_unit = party_controller.get_party_by_ru_ref(ru_ref)

        # Retrieve surveys for the reporting unit
        enrolments = [respondent['enrolments'] for respondent in reporting_unit.get('associations')]
        survey_ids = [enrolment['surveyId'] for enrolment in enrolments]
        surveys = [survey_controller.get_survey_by_id(survey_id) for survey_id in survey_ids]

        # Retrieve cases for the reporting unit
        cases = case_controller.get_case_groups_by_business_party_id(reporting_unit['id'])

        # Create required response data
        for survey in surveys:
            survey['collection_exercises'] = collection_exercise_controller.get_collection_exercises_by_survey(survey['id'])
            for exercise in survey['collection_exercise']:
                exercise['status'] = get_case_group_status_by_collection_exercise(cases, exercise['id'])

        response_json = {
            "reporting_unit": reporting_unit,
            "surveys": surveys
        }
        logger.info('Successfully retrieved reporting unit details', ru_ref=ru_ref)
        return make_response(jsonify(response_json), 200)
