import logging

from flask import jsonify, make_response
from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import collection_exercise_api
from ras_backstage.common.filters import filter_collection_exercises
from ras_backstage.controllers import collection_exercise_controller, survey_controller


logger = wrap_logger(logging.getLogger(__name__))


@collection_exercise_api.route('/<short_name>/<period>')
class GetSingleCollectionExercise(Resource):

    @staticmethod
    def get(short_name, period):
        logger.info('Retrieving collection exercise details', shortname=short_name, period=period)

        survey = survey_controller.get_survey_by_shortname(short_name)
        exercises = collection_exercise_controller.get_collection_exercises_by_survey(survey['id'])
        # Find the collection exercise for the given period
        exercise = filter_collection_exercises(exercises, period)
        if not exercise:
            return make_response(jsonify({"message": "Collection exercise not found"}), 404)
        full_exercise = collection_exercise_controller.get_collection_exercise_by_id(exercise['id'])

        response_json = {
            "survey": survey,
            "collection_exercise": full_exercise
        }
        logger.info('Successfully retrieved collection exercise details',
                    shortname=short_name, period=period)
        return make_response(jsonify(response_json), 200)
