import json
import logging
import unittest

import requests_mock

from ras_backstage import app


class TestSignIn(unittest.TestCase):
    def setUp(self):
        self.url_get_token = '{}{}'.format(app.config['RAS_OAUTH_SERVICE'],
                                           'api/v1/tokens/')
        self.app = app.test_client()
        self.headers = {
            'Content-Type': 'application/json',
        }
        self.posted_form = {'username': 'test', 'password': 'test'}
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
        mock_request.post(
            self.url_get_token, status_code=201, json=self.oauth2_response)

        response = self.app.post(
            '/backstage-api/v1/sign-in',
            headers=self.headers,
            data=json.dumps(self.posted_form))
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response_data.get('token'))

    @requests_mock.mock()
    def test_sign_in_oauth_fail(self, mock_request):
        mock_request.post(self.url_get_token, status_code=500)

        response = self.app.post(
            '/backstage-api/v1/sign-in',
            headers=self.headers,
            data=json.dumps(self.posted_form))
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)


class TestSignInV2(unittest.TestCase):
    def setUp(self):
        # Changing log level to DEBUG
        loglevel = logging.DEBUG
        logging.basicConfig(level=loglevel)

        self.app = app.test_client()

        self.data = json.dumps({
            'username': 'user',
            'password': 'pass',
        })

        self.wrong_user_data = json.dumps({
            'username': 'wrong',
            'password': 'pass',
        })

        self.wrong_pass_data = json.dumps({
            'username': 'user',
            'password': 'wrong',
        })

        self.all_wrong_data = json.dumps({
            'username': 'wrong',
            'password': 'also_wrong',
        })

        self.headers = {
            'Content-Type': 'application/json',
        }

    def test_sign_in_success(self):

        response = self.app.post(
            '/backstage-api/v2/sign-in', data=self.data, headers=self.headers)

        # response_json = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_sign_in_fails_wrong_user(self):
        data = {"username": "wrong", "password": "pass"}

        response = self.app.post(
            '/backstage-api/v2/sign-in',
            data=json.dumps(data),
            headers=self.headers)

        self.assertEqual(response.status_code, 401)

    def test_sign_in_fails_wrong_pass(self):
        response = self.app.post(
            '/backstage-api/v2/sign-in',
            data=self.wrong_user_data,
            headers=self.headers)

        self.assertEqual(response.status_code, 401)

    def test_sign_in_fails_wrong_user_and_pass(self):
        response = self.app.post(
            '/backstage-api/v2/sign-in',
            data=self.all_wrong_data,
            headers=self.headers)

        self.assertEqual(response.status_code, 401)

    def test_sign_in_fails_no_content_type(self):
        response = self.app.post(
            '/backstage-api/v2/sign-in', data=self.data, headers=None)

        self.assertEqual(response.status_code, 400)

    def test_sign_in_fails_no_content_type_wrong_user(self):
        response = self.app.post(
            '/backstage-api/v2/sign-in',
            data=self.wrong_user_data,
            headers=None)

        self.assertEqual(response.status_code, 400)

    def test_sign_in_fails_no_content_type_wrong_pass(self):
        response = self.app.post(
            '/backstage-api/v2/sign-in',
            data=self.wrong_pass_data,
            headers=None)

        self.assertEqual(response.status_code, 400)

    def test_sign_in_fails_no_content_type_wrong_pass_wrong_user(self):
        response = self.app.post(
            '/backstage-api/v2/sign-in',
            data=self.all_wrong_data,
            headers=None)

        self.assertEqual(response.status_code, 400)
