from flask import Blueprint, make_response, jsonify, current_app

from ras_backstage.controllers import controller
from ras_backstage.controllers.log_decorator import log_route


info_view = Blueprint('info_view', __name__)


@info_view.route('/info', methods=['GET'])
@log_route
def get_info():
    resp = controller.get_info(current_app.config)
    return make_response(jsonify(resp), 200)
