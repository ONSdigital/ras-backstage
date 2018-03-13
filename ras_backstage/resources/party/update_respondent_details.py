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
    'email_address': fields.String(required=True),
    'new_email_address': fields.String(required=True)
})


@party_api.route('/update-respondent-details/<respondent_id>')
class UpdateRespondentDetails(Resource):
    @staticmethod
    @party_api.expect(respondent_details, validate=True)
    def put(respondent_id):
        logger.info('Retrieving updated respondent details', respondent_id=respondent_id)
        respondent_contact_details = request.get_json()
        party_controller.update_respondent_details(respondent_id, respondent_contact_details)
        logger.info('Successfully updated user details', respondent_id=respondent_id)
        return 200
