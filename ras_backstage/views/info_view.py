from flask import Blueprint, make_response, jsonify, current_app

from ras_backstage.controllers import controller


info_view = Blueprint('info_view', __name__)


@info_view.route('/info', methods=['GET'])
def get_info():
    resp = controller.get_info(current_app.config)
    return make_response(jsonify(resp), 200)
