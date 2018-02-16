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


logger = wrap_logger(logging.getLogger(__name__))


@reporting_unit_api.route('/<ru_ref>')
class GetReportingUnit(Resource):

    @staticmethod
    def get(ru_ref):
        logger.info('Retrieving reporting unit details', ru_ref=ru_ref)

        # Get all collection exercises for ru_ref
        reporting_unit = party_controller.get_party_by_ru_ref(ru_ref)
        cases = case_controller.get_cases_by_business_party_id(reporting_unit['id'])
        collection_exercise_ids = [case['caseGroup']['collectionExerciseId']
                                   for case in cases]
        all_collection_exercises = [collection_exercise_controller.get_collection_exercise_by_id(collection_exercise_id)
                                    for collection_exercise_id in collection_exercise_ids]

        # We only want collection exercises which are live
        now = datetime.now(timezone.utc)
        collection_exercises = [collection_exercise
                                for collection_exercise in all_collection_exercises
                                if parse_date(collection_exercise['scheduledStartDateTime']) < now]

        # Add extra collection exercise details
        for exercise in collection_exercises:
            exercise['responseStatus'] = get_case_group_status_by_collection_exercise(cases, exercise['id'])
            reporting_unit_ce = party_controller.get_party_by_business_id(reporting_unit['id'], exercise['id'])
            exercise['companyName'] = reporting_unit_ce['name']
            exercise['companyRegion'] = reporting_unit_ce['region']

        # Get all surveys for gathered collection exercises
        survey_ids = {collection_exercise['surveyId']
                      for collection_exercise in collection_exercises}
        surveys = [survey_controller.get_survey_by_id(survey_id)
                   for survey_id in survey_ids]

        # Link collection exercises to surveys
        for survey in surveys:
            survey['collection_exercises'] = [collection_exercise
                                              for collection_exercise in collection_exercises
                                              if survey['id'] == collection_exercise['surveyId']]
            survey['respondents'] = []

        # Get respondents for ru_ref
        respondents = [party_controller.get_party_by_respondent_id(respondent['partyId'])
                       for respondent in reporting_unit.get('associations')]

        # Link respondents and surveys
        for respondent in respondents:
            respondent_survey_id_and_status = []
            for association in respondent.get('associations'):
                for enrolment in association.get('enrolments'):
                    respondent_survey_id_and_status.append(enrolment['surveyId'], )
            for survey in surveys:
                if survey['id'] in respondent_survey_ids:
                    survey['respondents'].append(respondent)
            respondent.pop('associations', None)




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
