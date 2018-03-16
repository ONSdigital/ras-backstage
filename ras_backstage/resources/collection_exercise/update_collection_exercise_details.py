import logging

from flask import request
from flask_restplus import Resource, fields
from structlog import wrap_logger

from ras_backstage import collection_exercise_api
from ras_backstage.controllers import collection_exercise_controller

logger = wrap_logger(logging.getLogger(__name__))

collection_exercise_details = collection_exercise_api.model('CollectionExerciseDetails', {
    'collectionExerciseID': fields.String(required=True),
    'exerciseRef': fields.String(required=True),
    'userDescription': fields.String(required=True)
})


@collection_exercise_api.route('/update-collection-exercise-details/')
class UpdateCollectionExerciseDetails(Resource):
    @staticmethod
    @collection_exercise_api.expect(collection_exercise_details, validate=True)
    def put(collection_exercise_id):

        logger.info('Retrieving updated collection exercise details')
        message_json = request.get_json()
        collection_exercise_id = message_json.get('collectionExerciseID')
        period = message_json.get('exerciseRef')
        shown_to_respondent_date = message_json.get('userDescription')

        collection_exercise_controller.update_collection_exercise_details(collection_exercise_id)

        logger.info('Successfully updated user details', collection_exercise_id=collection_exercise_id)

        return 200
