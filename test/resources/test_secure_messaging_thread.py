import json
import unittest

import requests_mock

from ras_backstage import app

url_get_thread = f"{app.config['RAS_SECURE_MESSAGING_SERVICE']}thread/78e3caa6-2e27-4ad3-bd38-168b2cc3ef5d"
with open('test/test_data/secure_messaging/thread.json') as json_data:
    thread = json.load(json_data)


class TestSecureMessaging(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = {
            'Authorization': 'test_jwt',
            'Content-Type': 'application/json',
        }

    @requests_mock.mock()
    def test_get_thread(self, mock_request):
        mock_request.get(url_get_thread, json=thread)
        message_url = "/backstage-api/v1/secure-message/threads" \
                      "/thread_id=78e3caa6-2e27-4ad3-bd38-168b2cc3ef5d"

        response = self.app.get(message_url, headers=self.headers)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response_data) == 3)