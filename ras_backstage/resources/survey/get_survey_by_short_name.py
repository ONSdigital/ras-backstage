import logging

from flask import jsonify, make_response
from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import survey_api
from ras_backstage.controllers import collection_exercise_controller, survey_controller


logger = wrap_logger(logging.getLogger(__name__))


@survey_api.route('/shortname/<string:short_name>')
class GetSurveyByShortName(Resource):

    @staticmethod
    def get(short_name):
        logger.info('Retrieving survey', short_name=short_name)

        survey = survey_controller.get_survey_by_shortname(short_name)
        collection_exercises = collection_exercise_controller.get_collection_exercises_by_survey(survey['id'])

        response_json = {"survey": survey, "collection_exercises": collection_exercises}

        logger.info('Successfully retrieved survey', survey_id=survey['id'], short_name=short_name)
        return make_response(jsonify(response_json), 200)
