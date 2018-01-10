import logging

from flask import jsonify, make_response, request
from flask_restplus import Resource, reqparse
from structlog import wrap_logger
from werkzeug.datastructures import FileStorage

from ras_backstage import sample_api
from ras_backstage.controllers import sample_controller


logger = wrap_logger(logging.getLogger(__name__))


parser = reqparse.RequestParser()
parser.add_argument('file', location='files', type=FileStorage, required=True)


@sample_api.route('/upload/<collection_exercise_id>')
class PostSampleFile(Resource):

    @staticmethod
    @sample_api.expect(parser)
    def post(collection_exercise_id):
        logger.info('Uploading sample file', collection_exercise_id=collection_exercise_id)

        # parser will return 400 if file (or collection_exercise_id arg) missing
        file_object = request.files['file']

        sample_id = sample_controller.post_sample_file_for_collection_exercise(collection_exercise_id,
                                                                               file_object.filename,
                                                                               file_object.read())

        logger.info('Successfully uploaded sample file', sample_id=sample_id)
        return make_response(jsonify(sample_id), 201)
