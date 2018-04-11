import logging

from flask import request
from flask_restplus import Resource, fields
from structlog import wrap_logger

from ras_backstage import survey_api
from ras_backstage.controllers import survey_controller

logger = wrap_logger(logging.getLogger(__name__))

survey_details = survey_api.model('SurveyDetails', {
    'short_name': fields.String(required=True),
    'long_name': fields.String(required=True)
})


@survey_api.route('/update-survey-details/<survey_ref>')
class UpdateSurveyDetails(Resource):
    @staticmethod
    @survey_api.expect(survey_details, validate=True)
    def put(survey_ref):

        logger.info('Retrieving updated survey details', survey_ref=survey_ref)
        updated_survey_details = request.get_json()
        survey_controller.update_survey_details(survey_ref, updated_survey_details)

        logger.info('Successfully updated survey details', survey_ref=survey_ref)

        return 200
