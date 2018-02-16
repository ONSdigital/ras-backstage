from datetime import datetime, timezone
import logging

from flask import jsonify, make_response
from flask_restplus import Resource
from iso8601 import parse_date
from structlog import wrap_logger

from ras_backstage import reporting_unit_api
from ras_backstage.common.filters import get_case_group_status_by_collection_exercise
from ras_backstage.controllers import (case_controller, collection_exercise_controller, party_controller,
                                       survey_controller)
from ras_backstage.controllers import iac_controller

logger = wrap_logger(logging.getLogger(__name__))


@reporting_unit_api.route('/<ru_ref>')
class GetReportingUnit(Resource):

    @staticmethod
    def get(ru_ref):
        logger.info('Retrieving reporting unit details', ru_ref=ru_ref)

        reporting_unit = party_controller.get_party_by_ru_ref(ru_ref)

        surveys = get_surveys_for_reporting_unit(reporting_unit)

        respondents_for_survey = get_respondents_for_reporting_unit(reporting_unit)

        cases = case_controller.get_cases_by_business_party_id(reporting_unit['id'])
        case_collection_exercise_ids = [case['caseGroup']['collectionExerciseId'] for case in cases]

        for survey in surveys:
            ces = collection_exercise_controller.get_collection_exercises_by_survey(survey['id'])
            now = datetime.now(timezone.utc)
            survey['collection_exercises'] = [ce for ce in ces
                                              if ce['id'] in case_collection_exercise_ids
                                              and parse_date(ce['scheduledStartDateTime']) < now]

            respondents = respondents_for_survey.get(survey.get('id'))
            survey['respondents'] = respondents if respondents else []

            ces_for_survey = list()
            # Add collection exercise details
            for exercise in survey['collection_exercises']:
                exercise['responseStatus'] = get_case_group_status_by_collection_exercise(cases, exercise['id'])
                reporting_unit_ce = party_controller.get_party_by_business_id(reporting_unit['id'], exercise['id'])
                exercise['companyName'] = reporting_unit_ce['name']
                exercise['companyRegion'] = reporting_unit_ce['region']
                ces_for_survey.append(exercise.get('id'))

            survey['activeIacCode'] = get_latest_activeiac_code(cases, ces_for_survey)

        response_json = {
            "reporting_unit": reporting_unit,
            "surveys": surveys
        }
        logger.info('Successfully retrieved reporting unit details', ru_ref=ru_ref)
        return make_response(jsonify(response_json), 200)


def get_surveys_for_reporting_unit(reporting_unit):
    survey_ids = []
    for respondent in reporting_unit.get('associations'):
        for enrolment in respondent.get('enrolments'):
            survey_ids.append(enrolment.get('surveyId'))
    unique_survey_ids = set(survey_ids)
    return [survey_controller.get_survey_by_id(survey_id) for survey_id in unique_survey_ids]


def get_respondents_for_reporting_unit(reporting_unit):
    respondents_per_survey = dict()
    for respondent in reporting_unit.get('associations'):
        respondent_details = party_controller.get_party_by_respondent_id(respondent.get('partyId'))
        respondent_details.pop('associations', None)
        for enrolment in respondent.get('enrolments'):
            respondent_details['enrolmentStatus'] = enrolment.get('enrolmentStatus')
            if enrolment.get('surveyId') in respondents_per_survey:
                respondents_per_survey[enrolment.get('surveyId')].append(respondent_details)
            else:
                respondents_per_survey[enrolment.get('surveyId')] = [respondent_details]
    return respondents_per_survey


def get_latest_activeiac_code(cases, ces_for_survey):
    cases_for_survey = []
    for case in cases:
        if case.get('caseGroup', {}).get('collectionExerciseId') in ces_for_survey:
            cases_for_survey.append(case)

    cases_for_survey = sorted(cases_for_survey, key=lambda c: c['createdDateTime'], reverse=True)

    for case in cases_for_survey:
        iac_details = iac_controller.get_iac(case.get('iac'))
        if iac_details.get('active'):
            return case.get('iac')
