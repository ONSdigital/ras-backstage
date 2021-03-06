from datetime import datetime, timezone
import logging

from flask import jsonify, make_response
from flask_restplus import Resource
from iso8601 import parse_date
from structlog import wrap_logger

from ras_backstage import reporting_unit_api
from ras_backstage.common.filters import get_case_group_status_by_collection_exercise
from ras_backstage.controllers import (case_controller, party_controller,
                                       survey_controller, iac_controller)
from ras_backstage.controllers.collection_exercise_controller import get_collection_exercise_by_id

logger = wrap_logger(logging.getLogger(__name__))


@reporting_unit_api.route('/<ru_ref>')
class GetReportingUnit(Resource):

    @staticmethod
    def get(ru_ref):
        logger.info('Retrieving reporting unit details', ru_ref=ru_ref)

        # Get all collection exercises for ru_ref
        reporting_unit = party_controller.get_party_by_ru_ref(ru_ref)
        case_groups = case_controller.get_case_groups_by_business_party_id(reporting_unit['id'])
        collection_exercise_ids = [case_group['collectionExerciseId'] for case_group in case_groups]
        collection_exercises = [get_collection_exercise_by_id(ce_id) for ce_id in collection_exercise_ids]

        # We only want collection exercises which are live
        now = datetime.now(timezone.utc)
        collection_exercises = [collection_exercise
                                for collection_exercise in collection_exercises
                                if parse_date(collection_exercise['scheduledStartDateTime']) < now]

        # Add extra collection exercise details using data from case service
        add_collection_exercise_details(collection_exercises, reporting_unit, case_groups)

        # Get all surveys for gathered collection exercises
        survey_ids = {collection_exercise['surveyId']
                      for collection_exercise in collection_exercises}
        surveys = [survey_controller.get_survey_by_id(survey_id)
                   for survey_id in survey_ids]

        # Get all respondents for the given ru
        respondents = [party_controller.get_party_by_respondent_id(respondent['partyId'])
                       for respondent in reporting_unit.get('associations')]

        # Link collection exercises and respondents to surveys
        cases = case_controller.get_cases_by_business_party_id(reporting_unit['id'])
        for survey in surveys:
            respondents_in_survey = [respondent
                                     for respondent in respondents
                                     if survey['id'] in survey_ids_for_respondent(respondent, ru_ref)]
            survey['respondents'] = [get_respondent_with_enrolment_status(respondent, ru_ref, survey['id'])
                                     for respondent in respondents_in_survey]
            survey['collection_exercises'] = [collection_exercise
                                              for collection_exercise in collection_exercises
                                              if survey['id'] == collection_exercise['surveyId']]
            survey['activeIacCode'] = get_latest_active_iac_code(survey['id'], cases, collection_exercises)

        response_json = {
            "reporting_unit": reporting_unit,
            "surveys": surveys
        }
        logger.info('Successfully retrieved reporting unit details', ru_ref=ru_ref)
        return make_response(jsonify(response_json), 200)


def survey_ids_for_respondent(respondent, ru_ref):
    enrolments = [association.get('enrolments')
                  for association in respondent.get('associations')
                  if association['sampleUnitRef'] == ru_ref][0]
    return [enrolment.get('surveyId') for enrolment in enrolments]


def get_respondent_with_enrolment_status(respondent, ru_ref, survey_id):
    association = next(association
                       for association in respondent.get('associations')
                       if association['sampleUnitRef'] == ru_ref)
    enrolment_status = next(enrolment['enrolmentStatus']
                            for enrolment in association.get('enrolments')
                            if enrolment['surveyId'] == survey_id)
    return {**respondent, 'enrolmentStatus': enrolment_status}


def add_collection_exercise_details(collection_exercises, reporting_unit, case_groups):
    for exercise in collection_exercises:
        exercise['responseStatus'] = get_case_group_status_by_collection_exercise(case_groups, exercise['id'])
        reporting_unit_ce = party_controller.get_party_by_business_id(reporting_unit['id'], exercise['id'])
        exercise['companyName'] = reporting_unit_ce['name']
        exercise['companyRegion'] = reporting_unit_ce['region']
        exercise['trading_as'] = reporting_unit_ce['trading_as']


def get_latest_active_iac_code(survey_id, cases, ces_for_survey):
    ces_ids = [ce['id'] for ce in ces_for_survey if survey_id == ce['surveyId']]
    cases_for_survey = [case
                        for case in cases
                        if case.get('caseGroup', {}).get('collectionExerciseId') in ces_ids]
    cases_for_survey_ordered = sorted(cases_for_survey, key=lambda c: c['createdDateTime'], reverse=True)
    iac = next((case.get('iac')
                for case in cases_for_survey_ordered
                if _is_iac_active(case.get('iac'))), None)
    return iac


def _is_iac_active(iac):
    iac_response = iac_controller.get_iac(iac)
    return iac_response.get('active') if iac_response else None
