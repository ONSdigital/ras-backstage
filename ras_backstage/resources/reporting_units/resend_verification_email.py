import logging

from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import reporting_unit_api
from ras_backstage.controllers import party_controller


logger = wrap_logger(logging.getLogger(__name__))


@reporting_unit_api.route('/resend-verification-email/<party_id>')
class ResendVerificationEmail(Resource):

    @staticmethod
    def post(party_id):
        logger.info('Attempting to resend verification email', party_id=party_id)
        party_controller.resend_verification_email(party_id)
        logger.info('Successfully resent verification email', party_id=party_id)
        return "OK", 200
