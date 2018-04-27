import logging

from flask import request
from flask_restplus import Resource, fields
from structlog import wrap_logger

from ras_backstage import collection_exercise_api
from ras_backstage.controllers import collection_exercise_controller

logger = wrap_logger(logging.getLogger(__name__))

collection_exercise_details = collection_exercise_api.model('CollectionExerciseDetails', {
    'survey_id': fields.String(required=True),
    'survey_name': fields.String(required=True),
    'user_description': fields.String(required=True),
    'period': fields.String(required=True)
})


@collection_exercise_api.route('/create-collection-exercise')
class CreateCollectionExercise(Resource):
    @staticmethod
    @collection_exercise_api.expect(collection_exercise_details, validate=True)
    def post():

        logger.info('Retrieving created collection exercise details')
        created_collection_exercise_details = request.get_json()
        collection_exercise_controller.create_collection_exercise(created_collection_exercise_details)

        logger.info('Successfully created new collection exercise')

        return 200
