import os

from flask import Flask
from flask_cors import CORS
from flask_restplus import Api, Namespace

from ras_backstage.logger_config import logger_initial_config

app = Flask(__name__)

app_config = 'config.{}'.format(os.environ.get('APP_SETTINGS', 'Config'))
app.config.from_object(app_config)

app.url_map.strict_slashes = False

logger_initial_config(service_name='ras-backstage', log_level=app.config['LOGGING_LEVEL'])

CORS(app)

api = Api(title='Ras-Backstage', default='info', default_label="")

sign_in_api = Namespace('sign-in', path='/backstage-api/v1/sign-in')
secure_messaging_api = Namespace('secure-messaging', path='/backstage-api/v1/secure-message')

api.add_namespace(sign_in_api)
api.add_namespace(secure_messaging_api)


import ras_backstage.error_handlers  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.info import Info  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.sign_in.sign_in import SignIn  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.secure_messaging.get_message_list import GetMessagesList  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.secure_messaging.get_message import GetMessage  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.secure_messaging.update_label import RemoveUnreadLabel  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.secure_messaging.send_message import SendMessage  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.secure_messaging.save_draft import SaveDraft  # NOQA # pylint: disable=wrong-import-position


api.init_app(app)
