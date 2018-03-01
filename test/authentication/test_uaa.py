import unittest

import requests_mock

from ras_backstage import app
from ras_backstage.authentication import uaa


class TestUaa(unittest.TestCase):

    def setUp(self):
        self.app = app
        app.config["UAA_PUBLIC_KEY"] = "Test"

    def test_get_uaa_public_key_with_config_set(self):
        with self.app.app_context():
            self.assertEqual("Test", uaa.get_uaa_public_key())

    @requests_mock.mock()
    def test_get_uaa_public_key_with_no_config_set(self, mock_request):
        mock_request.get(f'{app.config["UAA_SERVICE_URL"]}/token_key', json={'value':'Test'})
        app.config["UAA_PUBLIC_KEY"] = None
        with self.app.app_context():
            self.assertEqual("Test", uaa.get_uaa_public_key())