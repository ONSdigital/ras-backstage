import logging

from flask import request
from flask_restplus import fields, Resource
from structlog import wrap_logger

from ras_backstage import party_api
from ras_backstage.controllers import party_controller

logger = wrap_logger(logging.getLogger(__name__))

enrolment_details = party_api.model('EnrolmentDetails', {
    'respondent_id': fields.String(required=True),
    'business_id': fields.String(required=True),
    'survey_id': fields.String(required=True),
    'change_flag': fields.String(required=True)
})


@party_api.route('/change-enrolment-status')
class ChangeEnrolmentStatus(Resource):

    @staticmethod
    @party_api.expect(enrolment_details, validate=True)
    def put():
        enrolment_json = request.get_json()
        logger.info('Changing respondent enrolment status')

        party_controller.put_respondent_enrolment_status(enrolment_json)

        logger.info('Successfully changed enrolment status')
        return 200
