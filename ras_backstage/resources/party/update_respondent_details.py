import logging

from flask import jsonify, make_response, request
from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import party_api
from ras_backstage.controllers import party_controller


logger = wrap_logger(logging.getLogger(__name__))

@party_api.route('/party-update-respondent-details')
class RespondentDetails(Resource):

    @staticmethod
    @party_api.expect()
    def update():
        # logic todo
