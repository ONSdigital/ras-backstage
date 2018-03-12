import logging

from flask import request
from flask_restplus import Resource, fields
from structlog import wrap_logger

from ras_backstage import party_api
from ras_backstage.controllers import party_controller


logger = wrap_logger(logging.getLogger(__name__))

respondent_details = party_api.model('RespondentDetails', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'telephone': fields.String(required=True),
    'email': fields.String(required=True)       # TODO: Check if this is needed
})


@party_api.route('/update-respondent-details/<respondent_id>')
class UpdateRespondentDetails(Resource):
    @staticmethod
    @party_api.expect(respondent_details, validate=True)
    def put(respondent_id):

        logger.info('Retrieving updated respondent details')
        message_json = request.get_json()
        first_name = message_json.get('first_name')
        last_name = message_json.get('last_name')
        telephone = message_json.get('telephone')

        party_controller.update_respondent_details(respondent_id, first_name, last_name, telephone)

        # TODO: This block can just get passed from the UI (saves an API call to the party service)
        stored_email = party_controller.get_party_by_respondent_id(respondent_id).get('emailAddress')
        email = message_json.get('email')
        if email != stored_email:
            party_controller.update_respondent_email_address(respondent_id, stored_email, email)

        logger.info('Successfully updated user details', respondent_id=respondent_id)

        return 200
