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
        survey_ids = []
        for respondent in reporting_unit.get('associations'):
            for enrolment in respondent.get('enrolments'):
                survey_ids.append(enrolment.get('surveyId'))
        unique_survey_ids = set(survey_ids)
        surveys = [survey_controller.get_survey_by_id(survey_id) for survey_id in unique_survey_ids]

        # Retrieve cases for the reporting unit
        cases = case_controller.get_cases_by_business_party_id(reporting_unit['id'])
        case_collection_exercise_ids = [case['caseGroup']['collectionExerciseId'] for case in cases]

        for survey in surveys:
            survey_collection_exercises = []
            ces = collection_exercise_controller.get_collection_exercises_by_survey(survey['id'])
            for ce in ces:
                survey_collection_exercises.append(ce)
            survey['collection_exercises'] = [ce for ce in survey_collection_exercises if ce['id'] in case_collection_exercise_ids]

        for survey in surveys:
            for exercise in survey['collection_exercises']:
                exercise['responseStatus'] = get_case_group_status_by_collection_exercise(cases, exercise['id'])
                reporting_unit_ce = party_controller.get_party_by_business_id(reporting_unit['id'], exercise['id'])
                exercise['companyName'] = reporting_unit_ce['name']
                exercise['companyRegion'] = reporting_unit_ce['region']

        response_json = {
            "reporting_unit": reporting_unit,
            "surveys": surveys
        }
        logger.info('Successfully retrieved reporting unit details', ru_ref=ru_ref)
        return make_response(jsonify(response_json), 200)
