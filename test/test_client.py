import json

import yaml
from flask_testing import TestCase
from ras_common_utils.ras_config import ras_config
from ras_common_utils.ras_logger.ras_logger import configure_logger

from run import create_app
from test.fixtures.config import test_config


class TestClient(TestCase):
    config_data = yaml.load(test_config)
    config = ras_config.make(config_data)

    def create_app(self):
        self.app = create_app(self.config)
        configure_logger(self.app.config)
        return self.app

    def get_info(self, expected_status=200):
        response = self.client.open('/info', method='GET')
        self.assertStatus(response, expected_status)
        return json.loads(response.get_data(as_text=True))
