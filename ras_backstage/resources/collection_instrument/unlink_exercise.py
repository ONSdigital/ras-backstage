import logging

from flask import Response
from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import collection_instrument_api
from ras_backstage.controllers.collection_instrument_controller import unlink_collection_instrument_and_exercise


logger = wrap_logger(logging.getLogger(__name__))


@collection_instrument_api.route('/unlink/<collection_instrument_id>/<collection_exercise_id>')
class UnlinkExercise(Resource):

    @staticmethod
    def put(collection_instrument_id, collection_exercise_id):
        logger.info('Unlinking collection instrument and exercise',
                    collection_instrument_id=collection_instrument_id, collection_exercise_id=collection_exercise_id)
        unlink_collection_instrument_and_exercise(collection_instrument_id, collection_exercise_id)
        logger.info('Successfully unlinked collection instrument and exercise',
                    collection_instrument_id=collection_instrument_id, collection_exercise_id=collection_exercise_id)
        return Response(status=200)
