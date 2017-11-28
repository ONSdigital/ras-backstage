import json
import unittest

import requests_mock

from ras_backstage import app


url_get_token = app.config['OAUTH_TOKEN_URL']


class TestSignIn(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.posted_form = {
            'username': 'test',
            'password': 'test'
        }
        self.oauth2_response = {
            'id': 1,
            'access_token': '99a81f9c-e827-448b-8fa7-d563b76137ca',
            'expires_in': 3600,
            'token_type': 'Bearer',
            'scope': '',
            'refresh_token': 'a74fd471-6981-4503-9f59-00d45d339a15'
        }

    @requests_mock.mock()
    def test_sign_in_success(self, mock_request):
        mock_request.post(url_get_token, status_code=201, json=self.oauth2_response)

        response = self.app.post('/backstage-api/v1/sign-in', data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 201)
        self.assertTrue('"token"'.encode() in response.data)

    @requests_mock.mock()
    def test_sign_in_oauth_fail(self, mock_request):
        mock_request.post(url_get_token, status_code=500)

        response = self.app.post('/backstage-api/v1/sign-in', data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)
