import logging

from flask import jsonify, make_response
from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import survey_api
from ras_backstage.common.mappers import format_short_name
from ras_backstage.controllers import survey_controller


logger = wrap_logger(logging.getLogger(__name__))


@survey_api.route('/surveys')
class GetSurveyList(Resource):

    @staticmethod
    def get():
        logger.info('Retrieving survey list')

        survey_list = survey_controller.get_survey_list()

        # Format survey shortName
        for survey in survey_list:
            survey['shortName'] = format_short_name(survey['shortName'])

        logger.info('Successfully retrieved survey list')
        return make_response(jsonify(survey_list), 200)
