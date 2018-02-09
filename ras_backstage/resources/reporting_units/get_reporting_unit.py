import logging

from flask import jsonify, make_response
from flask_restplus import Resource
from structlog import wrap_logger

from ras_backstage import reporting_unit_api
from ras_backstage.controllers import party_controller


logger = wrap_logger(logging.getLogger(__name__))


@reporting_unit_api.route('/<ru_ref>')
class GetReportingUnit(Resource):

    @staticmethod
    def get(ru_ref):
        logger.info('Retrieving reporting unit details', ru_ref=ru_ref)
        reporting_unit = party_controller.get_party_by_ru_ref(ru_ref)
        logger.info('Successfully retrieved party details', ru_ref=ru_ref)
        return make_response(jsonify(reporting_unit), 200)
