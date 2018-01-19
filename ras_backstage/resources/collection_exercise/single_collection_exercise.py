import logging

from flask import jsonify, make_response
from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import collection_exercise_api
from ras_backstage.common.filters import get_collection_exercise_by_period
from ras_backstage.common.mappers import format_short_name

from ras_backstage.controllers import collection_exercise_controller, survey_controller
from ras_backstage.controllers.collection_instrument_controller import get_collection_instruments_by_classifier


logger = wrap_logger(logging.getLogger(__name__))


@collection_exercise_api.route('/<short_name>/<period>')
class GetSingleCollectionExercise(Resource):

    @staticmethod
    def get(short_name, period):
        logger.info('Retrieving collection exercise details', shortname=short_name, period=period)

        survey = survey_controller.get_survey_by_shortname(short_name)
        survey['shortName'] = format_short_name(survey['shortName'])

        exercises = collection_exercise_controller.get_collection_exercises_by_survey(survey['id'])
        # Find the collection exercise for the given period
        exercise = get_collection_exercise_by_period(exercises, period)
        if not exercise:
            return make_response(jsonify({"message": "Collection exercise not found"}), 404)
        full_exercise = collection_exercise_controller.get_collection_exercise_by_id(exercise['id'])

        exercise_events = collection_exercise_controller.get_collection_exercise_events(exercise['id'])

        collection_instruments = get_collection_instruments_by_classifier(survey['id'], exercise['id'])

        response_json = {
            "survey": survey,
            "collection_exercise": full_exercise,
            "events": exercise_events,
            "collection_instruments": collection_instruments
        }
        logger.info('Successfully retrieved collection exercise details',
                    shortname=short_name, period=period)
        return make_response(jsonify(response_json), 200)
