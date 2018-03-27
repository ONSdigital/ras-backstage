import logging

from flask import jsonify, make_response, request
from flask_restplus import fields, Resource
from structlog import wrap_logger

from ras_backstage import party_api
from ras_backstage.controllers import party_controller


logger = wrap_logger(logging.getLogger(__name__))

respondent_email = party_api.model('RespondentEmail', {
    'email': fields.String(required=True)
})


@party_api.route('/get-respondent-by-email')
class RespondentByEmail(Resource):

    @staticmethod
    @party_api.expect(respondent_email, validate=True)
    def get():
        logger.info('Get responddent by email')
        email = request.get_json()
        response = party_controller.get_respondent_by_email(email)

        logger.info("Successfully retrieved respondent by email")

        return make_response(jsonify(response), 200)