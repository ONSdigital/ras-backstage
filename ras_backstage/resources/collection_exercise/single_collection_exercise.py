import logging

from flask import jsonify, make_response
from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import collection_exercise_api
from ras_backstage.controllers import survey_controller


logger = wrap_logger(logging.getLogger(__name__))


@collection_exercise_api.route('/<short_name>/<period>')
class GetSingleCollectionExercise(Resource):

    @staticmethod
    def get(short_name, period):
        logger.info('Retrieving collection exercise details', shortname=short_name, period=period)

        survey = survey_controller.get_survey_by_shortname(short_name)

        logger.info('Successfully retrieved collection exercise details',
                    shortname=short_name, period=period)
        return make_response(jsonify(survey), 200)
