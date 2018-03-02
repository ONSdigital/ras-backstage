import json
import logging
import unittest

from ras_backstage import app


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
