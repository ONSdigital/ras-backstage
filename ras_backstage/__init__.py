import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_restplus import Api, Namespace

from ras_backstage.authentication.uaa import request_uaa_public_key
from ras_backstage.logger_config import logger_initial_config

app = Flask(__name__)

app_config = f"config.{os.environ.get('APP_SETTINGS', 'Config')}"
app.config.from_object(app_config)

app.url_map.strict_slashes = False

logger_initial_config(service_name='ras-backstage', log_level=app.config['LOGGING_LEVEL'])
logger = logging.getLogger(__name__)

if app.config.get('USE_UAA'):
    # cache the uaa public key on start up
    app.config['UAA_PUBLIC_KEY'] = request_uaa_public_key(app)

CORS(app)

api = Api(title='Ras-Backstage', default='info', default_label="")

collection_exercise_api = Namespace('collection-exercise',
                                    path='/backstage-api/v1/collection-exercise')
collection_instrument_api = Namespace('collection-instrument',
                                      path='/backstage-api/v1/collection-instrument')
party_api = Namespace('party', path='/backstage-api/v1/party')
reporting_unit_api = Namespace('reporting-unit', path='/backstage-api/v1/reporting-unit')
case_api = Namespace('case', path='/backstage-api/v1/case')
sample_api = Namespace('sample', path='/backstage-api/v1/sample')
secure_messaging_api = Namespace('secure-messaging',
                                 path='/backstage-api/v1/secure-message')
sign_in_api = Namespace('sign-in', path='/backstage-api/v1/sign-in')
sign_in_api_v2 = Namespace('sign-in-v2', path='/backstage-api/v2/sign-in')
survey_api = Namespace('survey', path='/backstage-api/v1/survey')

api.add_namespace(case_api)
api.add_namespace(collection_exercise_api)
api.add_namespace(collection_instrument_api)
api.add_namespace(party_api)
api.add_namespace(reporting_unit_api)
api.add_namespace(sample_api)
api.add_namespace(secure_messaging_api)
api.add_namespace(sign_in_api)
api.add_namespace(sign_in_api_v2)
api.add_namespace(survey_api)


import ras_backstage.error_handlers  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.collection_exercise.single_collection_exercise import GetSingleCollectionExercise, ExecuteSingleCollectionExercise  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.collection_instrument.collection_instrument import CollectionInstrument  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.collection_instrument.link_exercise import LinkExercise  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.info import Info  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.party.get_party_details import PartyDetails  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.reporting_units.get_reporting_unit import GetReportingUnit  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.reporting_units.generate_new_enrolment_code import GenerateNewEnrolmentCode  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.case.reporting_unit_case_group_status import ReportingUnitCaseGroupStatus  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.reporting_units.search_reporting_units import SearchReportingUnits  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.sample.sample import Sample  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.secure_messaging.get_message_list import GetMessagesList  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.secure_messaging.get_message import GetMessage  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.secure_messaging.update_label import RemoveUnreadLabel  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.secure_messaging.send_message import SendMessage  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.secure_messaging.save_draft import SaveDraft  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.secure_messaging.get_thread import GetThread  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.sign_in.sign_in import SignInV2  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.survey.get_survey_list import GetSurveyList  # NOQA # pylint: disable=wrong-import-position
from ras_backstage.resources.survey.get_survey_by_short_name import GetSurveyByShortName  # NOQA # pylint: disable=wrong-import-position


api.init_app(app)
