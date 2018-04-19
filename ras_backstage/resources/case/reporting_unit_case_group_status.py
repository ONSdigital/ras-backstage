import logging

from flask import jsonify, make_response, Response, request
from flask_restplus import Resource, fields
from structlog import wrap_logger

from ras_backstage import case_api
from ras_backstage.common.filters import get_collection_exercise_by_period, get_case_group_status_by_collection_exercise
from ras_backstage.common.mappers import format_short_name
from ras_backstage.controllers import survey_controller, collection_exercise_controller, party_controller, \
    case_controller
from ras_backstage.controllers.case_controller import get_available_statuses_for_ru_ref

logger = wrap_logger(logging.getLogger(__name__))


validate_enrolment_details = case_api.model('ValidateReportingUnitCaseGroupStatus', {
    'event': fields.String(required=True),
})


@case_api.route('/status/<short_name>/<period>/<ru_ref>')
class ReportingUnitCaseGroupStatus(Resource):

    @staticmethod
    def get(short_name, period, ru_ref):
        logger.info('Retrieving available statuses for reporting unit', short_name=short_name, period=period,
                    ru_ref=ru_ref)

        survey = survey_controller.get_survey_by_shortname(short_name)
        survey['shortName'] = format_short_name(survey['shortName'])

        # Get all collection exercises for ru_ref
        exercises = collection_exercise_controller.get_collection_exercises_by_survey(survey['id'])

        # Find the collection exercise for the given period
        exercise = get_collection_exercise_by_period(exercises, period)

        reporting_unit_details = party_controller.get_party_by_ru_ref(ru_ref)

        case_groups = case_controller.get_case_groups_by_business_party_id(reporting_unit_details['id'])

        current_status = get_case_group_status_by_collection_exercise(case_groups, exercise['id'])

        statuses = get_available_statuses_for_ru_ref(current_status, exercise['id'], ru_ref)

        response = {
            'ru_ref': ru_ref,
            'trading_as': reporting_unit_details['trading_as'],
            'survey_id': survey['surveyRef'],
            'short_name': short_name,
            'current_status': current_status,
            'available_statuses': statuses
        }

        logger.info('Successfully retrieved available statuses for reporting unit',
                    short_name=short_name, period=period, ru_ref=ru_ref)
        return make_response(jsonify(response), 200)

    @staticmethod
    @case_api.expect(validate_enrolment_details, validate=True)
    def post(short_name, period, ru_ref):
        logger.info('Updating available status', short_name=short_name, period=period,
                    ru_ref=ru_ref)
        body = request.json

        survey = survey_controller.get_survey_by_shortname(short_name)
        survey['shortName'] = format_short_name(survey['shortName'])

        # Get all collection exercises for ru_ref
        exercises = collection_exercise_controller.get_collection_exercises_by_survey(survey['id'])

        # Find the collection exercise for the given period
        exercise = get_collection_exercise_by_period(exercises, period)
        case_controller.update_case_group_status(exercise['id'], ru_ref, body['event'])

        logger.info('Successfully updated case group status for reporting unit', short_name=short_name, period=period,
                    ru_ref=ru_ref, case_group_event=body['event'])
        return Response(status=200)
