import logging

from flask import jsonify, make_response
from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import sample_api
from ras_backstage.common.filters import get_collection_exercise_by_period
from ras_backstage.controllers import collection_exercise_controller, sample_controller, survey_controller


logger = wrap_logger(logging.getLogger(__name__))


@sample_api.route('/<short_name>/<period>')
class Sample(Resource):

    @staticmethod
    def get(short_name, period):
        logger.info('Retrieving sample summary', shortname=short_name, period=period)

        survey = survey_controller.get_survey_by_shortname(short_name)
        exercises = collection_exercise_controller.get_collection_exercises_by_survey(survey['id'])
        # Find the collection exercise for the given period
        exercise = get_collection_exercise_by_period(exercises, period)
        if not exercise:
            return make_response(jsonify({'message': 'Collection exercise not found'}), 404)

        summary_id = collection_exercise_controller.get_linked_sample_summary_id(exercise['id'])

        sample_summary = sample_controller.get_sample_summary(summary_id)
        if not sample_summary:
            return make_response(jsonify({'message': 'Sample summary not found'}), 404)

        logger.info('Successfully retrieved sample summary details', shortname=short_name, period=period)
        return make_response(jsonify(sample_summary), 200)
