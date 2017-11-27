import os

from flask import Flask
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_restplus import Api, Namespace

from logger_config import logger_initial_config


app = Flask(__name__)

app_config = 'config.{}'.format(os.environ.get('APP_SETTINGS', 'Config'))
app.config.from_object(app_config)

app.url_map.strict_slashes = False

logger_initial_config(service_name='ras-frontstage-api', log_level=app.config['LOGGING_LEVEL'])

CORS(app)

auth = HTTPBasicAuth()

api = Api(title='Ras-Backstage', default='info', default_label=None)

sign_in_api = Namespace('sign-in', path='/backstage-api/v1/sign-in')
secure_messaging_api = Namespace('secure-messaging', path='/backstage-api/v1/secure-message')

api.add_namespace(sign_in_api)
api.add_namespace(secure_messaging_api)


@auth.get_password
def get_pw(username):
    config_username = app.config['SECURITY_USER_NAME']
    config_password = app.config['SECURITY_USER_PASSWORD']
    if username == config_username:
        return config_password


import ras_backstage.error_handlers  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.views.sign_in.sign_in import SignIn  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.views.secure_messaging.get_message_list import GetMessagesList  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.views.secure_messaging.get_message import GetMessage  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.views.secure_messaging.remove_unread_label import RemoveUnreadLabel  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.views.secure_messaging.send_message import SendMessage  # NOQA # pylint: disable=wrong-import-position


api.init_app(app)
