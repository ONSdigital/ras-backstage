import logging

from flask import jsonify, make_response, request
from flask_restplus import Resource, reqparse
from structlog import wrap_logger

from ras_backstage import party_api
from ras_backstage.controllers import party_controller


logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('query', location='args', required=True)


@party_api.route('/search-businesses')
class SearchBusinesses(Resource):

    @staticmethod
    @party_api.expect(parser)
    def get():
        query = request.args.get('query')

        logger.info('Retrieving businesses by search query', query=query)

        businesses = party_controller.get_businesses_by_search(query)

        logger.info('Successfully retrieved businesses by search query')
        return make_response(jsonify(businesses), 200)
