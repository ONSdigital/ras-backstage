import logging

from ras_common_utils.ras_config import ras_config
from structlog import wrap_logger

from ras_backstage.logger_config import logger_initial_config
from run import create_app

"""
This is a duplicate of run.py, with minor modifications to support gunicorn execution.
"""

logger = wrap_logger(logging.getLogger(__name__))


config_path = 'config/config.yaml'
with open(config_path) as f:
    config = ras_config.from_yaml_file(config_path)

app = create_app(config)
logger_initial_config()
logger.info("Created Flask app.")
logger.debug("Config is {}".format(app.config))

scheme, host, port = app.config['SCHEME'], app.config['HOST'], int(app.config['PORT'])
