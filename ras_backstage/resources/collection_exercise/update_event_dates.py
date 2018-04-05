import logging

from flask import jsonify, make_response, request, Response
from flask_restplus import fields, Resource
from structlog import wrap_logger

from ras_backstage import collection_exercise_api
from ras_backstage.common.filters import get_collection_exercise_by_period
from ras_backstage.controllers import collection_exercise_controller, survey_controller


logger = wrap_logger(logging.getLogger(__name__))


validate_event_timestamp = collection_exercise_api.model('ValidateUpdateEventDate', {
    'timestamp': fields.String(required=True)
})


@collection_exercise_api.route('/<short_name>/<period>/<tag>')
class UpdateEventDate(Resource):

    @staticmethod
    @collection_exercise_api.expect(validate_event_timestamp)
    def put(short_name, period, tag):
        logger.info('Updating event date', shortname=short_name, period=period, tag=tag)

        # Find the collection exercise id from shortname and period
        survey = survey_controller.get_survey_by_shortname(short_name)
        exercises = collection_exercise_controller.get_collection_exercises_by_survey(survey['id'])
        # Find the collection exercise for the given period
        exercise = get_collection_exercise_by_period(exercises, period)
        if not exercise:
            return make_response(jsonify({"message": "Collection exercise not found"}), 404)

        # Update the event timestamp
        timestamp = request.get_json().get('timestamp')
        collection_exercise_controller.update_event_date(exercise['id'], tag, timestamp)

        logger.info('Successfully updated event date', shortname=short_name, period=period, tag=tag)
        return Response(status=201)
