import logging

from flask import Response
from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import collection_instrument_api
from ras_backstage.controllers.collection_instrument_controller import link_collection_instrument_to_exercise


logger = wrap_logger(logging.getLogger(__name__))


@collection_instrument_api.route('/link/<collection_instrument_id>/<collection_exercise_id>')
class LinkExercise(Resource):

    @staticmethod
    def post(collection_instrument_id, collection_exercise_id):
        logger.info('Linking collection instrument to exercise',
                    collection_instrument_id=collection_instrument_id, collection_exercise_id=collection_exercise_id)
        link_collection_instrument_to_exercise(collection_instrument_id, collection_exercise_id)
        logger.info('Successfully linked collection instrument to exercise',
                    collection_instrument_id=collection_instrument_id, collection_exercise_id=collection_exercise_id)
        return Response(status=200)
