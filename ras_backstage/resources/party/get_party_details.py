import logging

from flask import jsonify, make_response, request
from flask_restplus import Resource, reqparse
from structlog import wrap_logger

from ras_backstage import party_api
from ras_backstage.controllers import party_controller


logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('business_party_id', location='args')
parser.add_argument('respondent_party_id', location='args')


@party_api.route('/party-details')
class PartyDetails(Resource):

    @staticmethod
    @party_api.expect(parser)
    def get():
        business_party_id = request.args.get('business_party_id')
        respondent_party_id = request.args.get('respondent_party_id')
        logger.info('Retrieving party details', business_party_id=business_party_id,
                    respondent_party_id=respondent_party_id)

        party_details = dict()

        if business_party_id:
            business_party = party_controller.get_party_by_business_id(business_party_id)
            party_details['business_party'] = business_party
        if respondent_party_id:
            respondent_party = party_controller.get_party_by_respondent_id(respondent_party_id)
            party_details['respondent_party'] = respondent_party

        logger.info('Successfully retrieved party details', business_party_id=business_party_id,
                    respondent_party_id=respondent_party_id)
        return make_response(jsonify(party_details), 200)
