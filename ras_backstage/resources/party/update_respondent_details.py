import logging

from flask import Response, request
from flask_restplus import Resource, fields
from structlog import wrap_logger

from ras_backstage import party_api
from ras_backstage.controllers import party_controller


logger = wrap_logger(logging.getLogger(__name__))

respondent_details = party_api.model('RespondentDetails', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'telephone': fields.String(required=True),
})


@party_api.route('/update-respondent-details')
class UpdateRespondentDetails(Resource):
    @staticmethod
    @party_api.expect(respondent_details)
    def post():

        logger.info('Retrieving updated respondent details')
        message_json = request.get_json()
        first_name = message_json.get('firstName')
        last_name = message_json.get('lastName')
        telephone = message_json.get('telephone')

        party_controller.update_respondent_details(id, first_name, last_name, telephone)
        logger.info('Successfully updated user details')

        return Response(status=200)
