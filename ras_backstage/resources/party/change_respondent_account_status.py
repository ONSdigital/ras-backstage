import logging

from flask import jsonify, make_response, request
from flask_restplus import fields, Resource
from structlog import wrap_logger

from ras_backstage import party_api
from ras_backstage.controllers import party_controller

logger = wrap_logger(logging.getLogger(__name__))

account_change_details = party_api.model('AccountDetails', {
    'party_id': fields.String(required=True),
    'status_change': fields.String(required=True)
})


@party_api.route('/change-respondent-account-status')
class ChangeAccountStatus(Resource):
    @staticmethod
    @party_api.expect(account_change_details, validate=True)
    def put():
        request_json = request.get_json()
        logger.info('Changing respondent account status')

        response = party_controller.change_respondent_account_status(request_json)

        logger.info('Successfully changed respondent account status', party_id=request_json['party_id'])
        return make_response(jsonify(response), 200)