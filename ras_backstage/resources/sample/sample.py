import logging

from flask import jsonify, make_response, request
from flask_restplus import Resource, reqparse
from structlog import wrap_logger

from ras_backstage import sample_api
from ras_backstage.common.filters import get_collection_exercise_by_period
from ras_backstage.controllers import collection_exercise_controller, sample_controller, survey_controller


logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('file', location='files', required=True)


@sample_api.route('/<short_name>/<period>')
class Sample(Resource):

    @staticmethod
    @sample_api.expect(parser)
    def post(short_name, period):
        logger.info('Uploading sample', shortname=short_name, period=period)

        survey = survey_controller.get_survey_by_shortname(short_name)
        exercises = collection_exercise_controller.get_collection_exercises_by_survey(survey['id'])
        # Find the collection exercise for the given period
        exercise = get_collection_exercise_by_period(exercises, period)
        if not exercise:
            return make_response(jsonify({'message': 'Collection exercise not found'}), 404)
        # Use the default 'B' for survey type
        sample_summary = sample_controller.upload_sample(exercise['id'], request.files['file'])
        logger.info('Successfully uploaded sample', sample_id=sample_summary['id'])

        logger.info('Linking sample summary with collection exercise',
                    collection_exercise_id=exercise['id'],
                    sample_id=sample_summary['id'])

        collection_exercise_controller.link_sample_summary_to_collection_exercise(
            collection_exercise_id=exercise['id'],
            sample_summary_id=sample_summary['id'])

        logger.info('Successfully linked sample to collection exercise',
                    collection_exercise_id=exercise['id'],
                    sample_id=sample_summary['id'])

        return make_response(jsonify(sample_summary), 201)
