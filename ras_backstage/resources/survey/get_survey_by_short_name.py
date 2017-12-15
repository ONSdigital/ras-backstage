import logging

from flask import jsonify, make_response
from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import survey_api
from ras_backstage.controllers import survey_controller


logger = wrap_logger(logging.getLogger(__name__))


@survey_api.route('/shortname/<string:short_name>')
class GetSurveyByShortName(Resource):

    @staticmethod
    def get(short_name):
        logger.info('Retrieving survey', short_name=short_name)

        survey = survey_controller.get_survey_by_shortname(short_name)

        logger.info('Successfully retrieved survey', short_name=short_name)
        return make_response(jsonify(survey), 200)
