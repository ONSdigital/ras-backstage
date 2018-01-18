import logging

from flask import jsonify, make_response, request
from flask_restplus import Resource, reqparse
from structlog import wrap_logger

from ras_backstage import sample_api
from ras_backstage.controllers import collection_exercise_controller, sample_controller, survey_controller


logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('file', location='files', required=True)
parser.add_argument('collection_exercise_id', location='args', required=True)


@sample_api.route('')
class Sample(Resource):

    @staticmethod
    @sample_api.expect(parser)
    def post():
        collection_exercise_id = request.args.get('collection_exercise_id')
        if not collection_exercise_id:
            return make_response(jsonify({'message': 'Missing collection_exercise_id'}), 400)

        logger.info('Uploading sample', collection_exercise_id=collection_exercise_id)

        exercise = collection_exercise_controller.get_collection_exercise_by_id(collection_exercise_id)
        if not exercise:
            return make_response(jsonify({'message': 'Collection exercise not found'}), 404)
        # Use the default 'B' for survey type
        response_json = sample_controller.upload_sample(exercise['id'], request.files['file'])

        logger.info('Successfully uploaded sample', collection_exercise_id=collection_exercise_id)
        return make_response(jsonify(response_json), 201)
