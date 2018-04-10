import logging

from flask import jsonify, make_response
from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import survey_api
from ras_backstage.common.mappers import format_short_name
from ras_backstage.controllers import collection_exercise_controller, survey_controller, sample_controller


logger = wrap_logger(logging.getLogger(__name__))


@survey_api.route('/shortname/<string:short_name>')
class GetSurveyByShortName(Resource):

    @staticmethod
    def get(short_name):
        logger.info('Retrieving survey', short_name=short_name)

        survey = survey_controller.get_survey_by_shortname(short_name)
        # Format survey shortName
        survey['shortName'] = format_short_name(survey['shortName'])

        ce_list = collection_exercise_controller.get_collection_exercises_by_survey(survey['id'])
        GetSurveyByShortName.add_events(ce_list)
        GetSurveyByShortName.add_sample_summary(ce_list)
        response_json = {"survey": survey, "collection_exercises": ce_list}

        logger.info('Successfully retrieved survey', survey_id=survey['id'], short_name=short_name)
        return make_response(jsonify(response_json), 200)

    @staticmethod
    def add_events(ce_list):
        for ce in ce_list:
            ce['events'] = collection_exercise_controller.get_collection_exercise_events(ce['id'])

    @staticmethod
    def add_sample_summary(ce_list):
        for ce in ce_list:
            sample_summary_id = collection_exercise_controller.get_linked_sample_summary_id(ce['id'])
            if sample_summary_id:
                ce['sample_summary'] = sample_controller.get_sample_summary(sample_summary_id)
