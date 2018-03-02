import json
import unittest

import requests_mock

from ras_backstage import app


url_get_message = '{}{}{}'.format(app.config['RAS_SECURE_MESSAGING_SERVICE'],
                                  'message/', 'dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b')
with open('test/test_data/secure_messaging/message.json') as json_data:
    message = json.load(json_data)
url_get_messages = '{}{}{}'.format(app.config['RAS_SECURE_MESSAGING_SERVICE'],
                                   'v2/messages', '?label=INBOX&limit=1000')
with open('test/test_data/secure_messaging/messages_list.json') as json_data:
    messages_list = json.load(json_data)
url_update_label = '{}{}'.format(app.config['RAS_SECURE_MESSAGING_SERVICE'],
                                 'message/{}/modify'.format('dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b'))
url_send_message = '{}{}'.format(app.config['RAS_SECURE_MESSAGING_SERVICE'], 'v2/messages')
url_save_draft = '{}{}'.format(app.config['RAS_SECURE_MESSAGING_SERVICE'], 'draft/save')
url_modify_draft = '{}{}'.format(app.config['RAS_SECURE_MESSAGING_SERVICE'],
                                 'draft/{}/modify'.format('test_msg_id'))


class TestSecureMessaging(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = {
            'Authorization': 'test_jwt',
            'Content-Type': 'application/json',
        }
        self.posted_message = {
            'msg_from': '07d672bc-497b-448f-a406-a20a7e6013d7',
            'subject': 'test-subject',
            'body': 'test-body',
            'thread_id': ''
        }
        self.sent_message_response = {
            'msg_id': '36f3133c-9ead-4168-a40e-f07947671b02',
            'status': '201',
            'thread_id': '8caeff79-6067-4f2a-96e0-08617fdeb496'
        }

    @requests_mock.mock()
    def test_get_message(self, mock_request):
        mock_request.get(url_get_message, json=message)
        message_url = "/backstage-api/v1/secure-message/message" \
                      "?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&is_draft=false"

        response = self.app.get(message_url, headers=self.headers)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['body'], "TEsdfdsfST")

    @requests_mock.mock()
    def test_get_message_fail(self, mock_request):
        mock_request.get(url_get_message, status_code=500)
        message_url = "/backstage-api/v1/secure-message/message" \
                      "?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&is_draft=false"

        response = self.app.get(message_url, headers=self.headers)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_message_list(self, mock_request):
        mock_request.get(url_get_messages, json=messages_list)
        message_url = "/backstage-api/v1/secure-message/messages?limit=1000&label=INBOX"

        response = self.app.get(message_url, headers=self.headers)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['messages'][0]['body'], "TEsdfdsfST")

    @requests_mock.mock()
    def test_get_message_list_fail(self, mock_request):
        mock_request.get(url_get_messages, status_code=500)
        message_url = "/backstage-api/v1/secure-message/messages?limit=1000&label=INBOX"

        response = self.app.get(message_url, headers=self.headers)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_update_label(self, mock_request):
        mock_request.put(url_update_label)
        url = '/backstage-api/v1/secure-message/update-label/dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b'

        response = self.app.put(url, headers=self.headers,
                                data=json.dumps({"label": 'UNREAD', "action": "remove"}))

        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_remove_unread_label_fail(self, mock_request):
        mock_request.put(url_update_label, status_code=500)
        url = '/backstage-api/v1/secure-message/update-label/dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b'

        response = self.app.put(url, headers=self.headers,
                                data=json.dumps({"label": 'UNREAD', "action": "remove"}))
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_send_message(self, mock_request):
        mock_request.post(url_send_message, json=self.sent_message_response, status_code=201)
        url = '/backstage-api/v1/secure-message/send-message'

        response = self.app.post(url, headers=self.headers, data=json.dumps(self.posted_message))
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['status'], "201")

    @requests_mock.mock()
    def test_send_message_fail(self, mock_request):
        mock_request.post(url_send_message, status_code=500)
        url = '/backstage-api/v1/secure-message/send-message'

        response = self.app.post(url, headers=self.headers, data=json.dumps(self.posted_message))
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_save_draft(self, mock_request):
        mock_request.post(url_save_draft, json=self.sent_message_response, status_code=201)
        url = '/backstage-api/v1/secure-message/save-draft'

        response = self.app.post(url, headers=self.headers, data=json.dumps(self.posted_message))
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['status'], "201")

    @requests_mock.mock()
    def test_save_draft_fail(self, mock_request):
        mock_request.post(url_save_draft, status_code=500)
        url = '/backstage-api/v1/secure-message/save-draft'

        response = self.app.post(url, headers=self.headers, data=json.dumps(self.posted_message))
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_update_draft(self, mock_request):
        mock_request.put(url_modify_draft, json=self.sent_message_response, status_code=200)
        self.posted_message['msg_id'] = 'test_msg_id'
        self.sent_message_response['status'] = '200'
        url = '/backstage-api/v1/secure-message/save-draft'

        response = self.app.put(url, headers=self.headers, data=json.dumps(self.posted_message))
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], "200")

    @requests_mock.mock()
    def test_update_draft_fail(self, mock_request):
        mock_request.put(url_modify_draft, status_code=500)
        self.posted_message['msg_id'] = 'test_msg_id'
        url = '/backstage-api/v1/secure-message/save-draft'

        response = self.app.put(url, headers=self.headers, data=json.dumps(self.posted_message))
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)
