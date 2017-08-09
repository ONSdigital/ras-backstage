from flask import make_response, jsonify, current_app
from structlog import get_logger

from ras_backstage.controllers.error_decorator import translate_exceptions

log = get_logger()


# TODO: consider a decorator to get a db session where needed (maybe replace transaction context mgr)


@translate_exceptions
def get_info():
    info = {
        "name": current_app.config['NAME'],
        "version": current_app.config['VERSION'],
        "origin": "git@github.com:ONSdigital/ras-backstage.git",
        "commit": "TBD",
        "branch": "TBD",
        "built": "TBD"
    }

    if current_app.config.feature.report_dependencies:
        info["dependencies"] = [{'name': name} for name in current_app.config.dependency.keys()]

    return make_response(jsonify(info), 200)
