import logging

from flask import make_response, jsonify, request, Response
from flask_restplus import Resource, reqparse
from structlog import wrap_logger

from ras_backstage import collection_instrument_api
from ras_backstage.common.filters import get_collection_exercise_by_period
from ras_backstage.controllers import survey_controller, collection_exercise_controller
from ras_backstage.controllers.collection_instrument_controller import upload_collection_instrument


logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('file', location='files', required=True)
parser.add_argument('classifiers', location='args')


@collection_instrument_api.route('/<short_name>/<period>')
class CollectionInstrument(Resource):

    @staticmethod
    @collection_instrument_api.expect(parser)
    def post(short_name, period):
        logger.info('Uploading collection instrument', shortname=short_name, period=period)
        survey = survey_controller.get_survey_by_shortname(short_name)
        exercises = collection_exercise_controller.get_collection_exercises_by_survey(survey['id'])
        # Find the collection exercise for the given period
        exercise = get_collection_exercise_by_period(exercises, period)
        if not exercise:
            return make_response(jsonify({"message": "Collection exercise not found"}), 404)

        upload_collection_instrument(exercise['id'], request.files['file'], request.args)

        logger.info('Successfully uploaded collection instrument', shortname=short_name, period=period)
        return Response(status=201)
