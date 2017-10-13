import logging
from json import loads
from pathlib import Path

from flask import jsonify
from flask_cors import CORS
from ras_backstage.logger_config import logger_initial_config
from ras_backstage.ras_config import ras_config
from ras_backstage.ras_config.flask_extended import Flask
from ras_backstage.exception.exceptions import RasError
from structlog import wrap_logger

logger = wrap_logger(logging.getLogger(__name__))


def create_app(config):
    # create and configure the Flask app
    app = Flask(__name__)
    app.config.from_ras_config(config)

    if Path('git_info').exists():
        with open('git_info') as io:
            service_metadata = loads(io.read())
            app.config['METADATA'] = service_metadata

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
    logger_initial_config(app.config)

    logger.debug("Created Flask app.")
    logger.debug("Config is {}".format(app.config))

    scheme, host, port = app.config['SCHEME'], app.config['HOST'], int(app.config['PORT'])

    app.run(debug=app.config['DEBUG'], host=host, port=port)
