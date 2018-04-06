import logging

from flask import jsonify, make_response, request, Response
from flask_restplus import fields, Resource
from structlog import wrap_logger

from ras_backstage import collection_exercise_api
from ras_backstage.controllers.collection_exercise_controller import get_collection_exercise_and_survey, \
    get_collection_exercise_events, update_event_date


logger = wrap_logger(logging.getLogger(__name__))


validate_event_timestamp = collection_exercise_api.model('ValidateUpdateEventDate', {
    'timestamp': fields.String(required=True)
})


@collection_exercise_api.route('/<short_name>/<period>/update-events')
@collection_exercise_api.route('/<short_name>/<period>/update-events/<tag>')
class UpdateEventDate(Resource):

    @staticmethod
    def get(short_name, period):
        logger.info('Retrieving data for update event date page',
                    shortname=short_name, period=period)

        survey_exercise = get_collection_exercise_and_survey(short_name, period)
        collection_exercise = survey_exercise['collection_exercise']
        if not collection_exercise:
            return make_response(jsonify({"message": "Collection exercise not found"}), 404)
        events = get_collection_exercise_events(collection_exercise['id'])

        response_json = {
            **survey_exercise,
            "events": events
        }
        logger.info('Successfully retrieved data for update event date page',
                    shortname=short_name, period=period)
        return make_response(jsonify(response_json), 200)

    @staticmethod
    @collection_exercise_api.expect(validate_event_timestamp)
    def put(short_name, period, tag):
        logger.info('Updating event date', shortname=short_name, period=period, tag=tag)

        # Find the collection exercise id from shortname and period
        collection_exercise = get_collection_exercise_and_survey(short_name, period)['collection_exercise']
        if not collection_exercise:
            return make_response(jsonify({"message": "Collection exercise not found"}), 404)

        # Update the event timestamp
        json = request.get_json()
        timestamp = json.get('timestamp')
        update_event_date(collection_exercise['id'], tag, timestamp)

        logger.info('Successfully updated event date', shortname=short_name, period=period, tag=tag)
        return Response(status=201)
