import json
import logging
import unittest

from ras_backstage import app


url_get_token = '{}{}'.format(app.config['RAS_OAUTH_SERVICE'], 'api/v1/tokens/')


class TestSignInUAA(unittest.TestCase):

    def setUp(self):
        # Changing log level to DEBUG
        loglevel = logging.DEBUG
        logging.basicConfig(level=loglevel)

        self.app = app.test_client()

        self.headers = {
            'Content-Type': 'application/json',
        }

    def test_sign_in_success(self):
        data = {
            'username': 'user',
            'password': 'pass',
        }

        response = self.app.post('/backstage-api/v1/sign-in-uaa',
                                 data=json.dumps(data),
                                 headers=self.headers)

        # response_json = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

    def test_sign_in_fails(self):
        data = {
            "username": "wrong",
            "password": "pass"
        }

        response = self.app.post('/backstage-api/v1/sign-in-uaa',
                                 data=json.dumps(data),
                                 headers=self.headers)

        # response_json = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
