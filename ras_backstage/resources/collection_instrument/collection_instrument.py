import logging

from flask import make_response, jsonify, request
from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import collection_instrument_api
from ras_backstage.common.filters import get_collection_exercise_by_period
from ras_backstage.controllers import survey_controller, collection_exercise_controller, \
    collection_instrument_controller

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

        collection_instrument_controller.upload_collection_instrument(survey['id'], exercise['id'], request.files['file'])
