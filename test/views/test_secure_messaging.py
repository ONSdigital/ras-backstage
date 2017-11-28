import json
import unittest

import requests_mock

from ras_backstage import app


url_get_message = '{}{}{}'.format(app.config['SECURE_MESSAGING_SERVICE'], 'message/', 'dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b')
with open('test/test_data/secure_messaging/message.json') as json_data:
    message = json.load(json_data)
url_get_messages = '{}{}{}'.format(app.config['SECURE_MESSAGING_SERVICE'], 'messages', '?label=INBOX&limit=1000')
with open('test/test_data/secure_messaging/messages_list.json') as json_data:
    messages_list = json.load(json_data)
url_remove_unread_label = '{}{}'.format(app.config['SECURE_MESSAGING_SERVICE'], 'message/{}/modify'.format('dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b'))
url_send_message = '{}{}'.format(app.config['SECURE_MESSAGING_SERVICE'], 'message/send')
url_save_draft = '{}{}'.format(app.config['SECURE_MESSAGING_SERVICE'], 'draft/save')
url_modify_draft = '{}{}'.format(app.config['SECURE_MESSAGING_SERVICE'], 'draft/{}/modify'.format('test_msg_id'))


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
        message_url = "/backstage-api/v1/secure-message/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&is_draft=false"

        response = self.app.get(message_url, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"body": "TEsdfdsfST"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_fail(self, mock_request):
        mock_request.get(url_get_message, status_code=500)
        message_url = "/backstage-api/v1/secure-message/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&is_draft=false"

        response = self.app.get(message_url, headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_list(self, mock_request):
        mock_request.get(url_get_messages, json=messages_list)
        message_url = "/backstage-api/v1/secure-message/messages?limit=1000&label=INBOX"

        response = self.app.get(message_url, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"body": "TEsdfdsfST"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_list_fail(self, mock_request):
        mock_request.get(url_get_messages, status_code=500)
        message_url = "/backstage-api/v1/secure-message/messages?limit=1000&label=INBOX"

        response = self.app.get(message_url, headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_remove_unread_label(self, mock_request):
        mock_request.put(url_remove_unread_label)

        response = self.app.put('/backstage-api/v1/secure-message/remove-unread?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_remove_unread_label_fail(self, mock_request):
        mock_request.put(url_remove_unread_label, status_code=500)

        response = self.app.put('/backstage-api/v1/secure-message/remove-unread?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b', headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_send_message(self, mock_request):
        mock_request.post(url_send_message, json=self.sent_message_response, status_code=201)

        response = self.app.post('/backstage-api/v1/secure-message/send-message', headers=self.headers, data=json.dumps(self.posted_message))

        self.assertEqual(response.status_code, 201)
        self.assertTrue('"status": "201"'.encode() in response.data)

    @requests_mock.mock()
    def test_send_message_fail(self, mock_request):
        mock_request.post(url_send_message, status_code=500)

        response = self.app.post('/backstage-api/v1/secure-message/send-message', headers=self.headers, data=json.dumps(self.posted_message))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_save_draft(self, mock_request):
        mock_request.post(url_save_draft, json=self.sent_message_response, status_code=201)

        response = self.app.post('/backstage-api/v1/secure-message/save-draft', headers=self.headers, data=json.dumps(self.posted_message))

        self.assertEqual(response.status_code, 201)
        self.assertTrue('"status": "201"'.encode() in response.data)

    @requests_mock.mock()
    def test_save_draft_fail(self, mock_request):
        mock_request.post(url_save_draft, status_code=500)

        response = self.app.post('/backstage-api/v1/secure-message/save-draft', headers=self.headers, data=json.dumps(self.posted_message))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_update_draft(self, mock_request):
        mock_request.put(url_modify_draft, json=self.sent_message_response, status_code=200)
        self.posted_message['msg_id'] = 'test_msg_id'
        self.sent_message_response['status'] = '200'

        response = self.app.put('/backstage-api/v1/secure-message/save-draft', headers=self.headers, data=json.dumps(self.posted_message))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"status": "200"'.encode() in response.data)

    @requests_mock.mock()
    def test_update_draft_fail(self, mock_request):
        mock_request.put(url_modify_draft, status_code=500)
        self.posted_message['msg_id'] = 'test_msg_id'

        response = self.app.put('/backstage-api/v1/secure-message/save-draft', headers=self.headers, data=json.dumps(self.posted_message))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)
