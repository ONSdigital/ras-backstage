import logging

from flask import make_response, jsonify, request, Response
from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import collection_instrument_api
from ras_backstage.common.filters import get_collection_exercise_by_period
from ras_backstage.controllers import survey_controller, collection_exercise_controller
from ras_backstage.controllers.collection_instrument_controller import get_collection_instruments_by_classifier, \
    upload_collection_instrument

logger = wrap_logger(logging.getLogger(__name__))


@collection_instrument_api.route('/<short_name>/<period>')
class CollectionInstrument(Resource):

    @staticmethod
    def post(short_name, period):
        logger.info('Uploading collection instrument', shortname=short_name, period=period)
        survey = survey_controller.get_survey_by_shortname(short_name)
        exercises = collection_exercise_controller.get_collection_exercises_by_survey(survey['id'])
        # Find the collection exercise for the given period
        exercise = get_collection_exercise_by_period(exercises, period)
        if not exercise:
            return make_response(jsonify({"message": "Collection exercise not found"}), 404)

        upload_collection_instrument(survey['id'], exercise['id'], request.files['file'])
        logger.info('Successfully retrieved collection exercise details', shortname=short_name, period=period)
        return Response(status=201)

    @staticmethod
    def get(short_name, period):
        logger.info('Retrieving collection instruments', short_name=short_name, period=period)

        survey = survey_controller.get_survey_by_shortname(short_name)
        exercises = collection_exercise_controller.get_collection_exercises_by_survey(survey['id'])
        # Find the collection exercise for the given period
        exercise = get_collection_exercise_by_period(exercises, period)
        if not exercise:
            return make_response(jsonify({"message": "Collection exercise not found"}), 404)
        collection_instruments = get_collection_instruments_by_classifier(survey['id'], exercise['id'])

        logger.info('Successfully retrieved collection instruments', short_name=short_name, period=period)
        return make_response(jsonify(collection_instruments), 200)
