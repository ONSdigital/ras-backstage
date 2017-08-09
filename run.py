import structlog
from flask import jsonify
from flask_cors import CORS
from ras_common_utils.ras_config import ras_config
from ras_common_utils.ras_config.flask_extended import Flask
from ras_common_utils.ras_logger.ras_logger import configure_logger

from ras_backstage.controllers.ras_error import RasError

logger = structlog.get_logger()


def create_app(config):
    # create and configure the Flask app
    app = Flask(__name__)
    app.config.from_ras_config(config)

    @app.errorhandler(Exception)
    def handle_error(error):
        if isinstance(error, RasError):
            response = jsonify(error.to_dict())
            response.status_code = error.status_code
        else:
            response = jsonify({'errors': [str(error)]})
            response.status_code = 500
        return response

    # register view blueprints
    from ras_backstage.views.backstage_view import backstage_view
    from ras_backstage.views.info_view import info_view
    app.register_blueprint(backstage_view, url_prefix='/backstage-api/v1')
    app.register_blueprint(info_view)

    CORS(app)
    return app


if __name__ == '__main__':
    config_path = 'config/config.yaml'
    with open(config_path) as f:
        config = ras_config.from_yaml_file(config_path)

    app = create_app(config)
    configure_logger(app.config)
    logger.debug("Created Flask app.")
    logger.debug("Config is {}".format(app.config))

    scheme, host, port = app.config['SCHEME'], app.config['HOST'], int(app.config['PORT'])

    app.run(debug=app.config['DEBUG'], host=host, port=port)
