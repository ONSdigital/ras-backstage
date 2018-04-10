import logging

from flask import jsonify, make_response, request, Response
from flask_restplus import fields, Resource
from structlog import wrap_logger

from ras_backstage import collection_exercise_api
from ras_backstage.controllers.collection_exercise_controller import get_collection_exercise_and_survey, \
    get_collection_exercise_events, update_event, create_event


logger = wrap_logger(logging.getLogger(__name__))


validate_event_timestamp = collection_exercise_api.model('ValidateUpdateEventDate', {
    'timestamp': fields.String(required=True)
})


@collection_exercise_api.route('/<short_name>/<period>/events')
@collection_exercise_api.route('/<short_name>/<period>/events/<tag>')
class CollectionExerciseEvents(Resource):

    @staticmethod
    def get(short_name, period):
        logger.info('Retrieving data for collection exercise events',
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
        logger.info('Successfully got collection exercise events',
                    shortname=short_name, period=period)
        return make_response(jsonify(response_json), 200)

    @staticmethod
    @collection_exercise_api.expect(validate_event_timestamp)
    def put(short_name, period, tag):
        logger.info('Updating event', shortname=short_name, period=period, tag=tag)

        # Find the collection exercise id from shortname and period
        collection_exercise = get_collection_exercise_and_survey(short_name, period)['collection_exercise']
        if not collection_exercise:
            return make_response(jsonify({"message": "Collection exercise not found"}), 404)

        # Update the event timestamp
        json = request.get_json()
        timestamp = json.get('timestamp')
        update_event(collection_exercise['id'], tag, timestamp)

        logger.info('Successfully updated event', shortname=short_name, period=period, tag=tag)
        return Response(status=201)

    @staticmethod
    @collection_exercise_api.expect(validate_event_timestamp)
    def post(short_name, period, tag):
        logger.info('Creating event', short_name=short_name, period=period, tag=tag)

        # Find the collection exercise id from shortname and period
        collection_exercise = get_collection_exercise_and_survey(short_name, period)['collection_exercise']
        if not collection_exercise:
            return make_response(jsonify({"message": "Collection exercise not found"}), 404)

        json = request.get_json()
        timestamp = json.get('timestamp')
        event = {
            'tag': tag,
            'timestamp': timestamp,
            'collectionExerciseId': collection_exercise['id']  # Don't actually need it gets set again in the end point
        }
        create_event(collection_exercise['id'], tag, event)

        logger.info('Successfully created event', shortname=short_name, period=period, tag=tag)
        return Response(status=201)

