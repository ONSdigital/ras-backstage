import logging

from flask import request
from flask_restplus import Resource, fields
from structlog import wrap_logger

from ras_backstage import collection_exercise_api
from ras_backstage.controllers import collection_exercise_controller

logger = wrap_logger(logging.getLogger(__name__))

collection_exercise_details = collection_exercise_api.model('CollectionExerciseDetails', {
    'user_description': fields.String(required=True),
    'period': fields.String(required=True)
})


@collection_exercise_api.route('/update-collection-exercise-details/<collection_exercise_id>')
class UpdateCollectionExerciseDetails(Resource):
    @staticmethod
    @collection_exercise_api.expect(collection_exercise_details, validate=True)
    def put(collection_exercise_id):

        logger.info('Retrieving updated collection exercise details', collection_exercise_id=collection_exercise_id)
        user_description = request.json["user_description"]
        period = request.json["period"]

        collection_exercise_controller.update_collection_exercise_user_description(collection_exercise_id,
                                                                                   user_description)

        collection_exercise_controller.update_collection_exercise_period(collection_exercise_id, period)

        logger.info('Successfully updated collection exercise details', collection_exercise_id=collection_exercise_id)

        return 200
