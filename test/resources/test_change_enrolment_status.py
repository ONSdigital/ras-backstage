import json
import unittest

import requests_mock

from ras_backstage import app


url_change_enrolment_status = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/respondents/change_enrolment_status'


class TestChangeEnrolmentStatus(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.enrolment_details = {
            'respondent_id': 'test_id',
            'business_id': 'test_id',
            'survey_id': 'test_id',
            'change_flag': 'RESPONDENT_ENROLMENT_DISABLED'
        }
        self.headers = {
            'Content-Type': 'application/json',
        }

    @requests_mock.mock()
    def test_change_enrolment_status(self, mock_request):
        mock_request.put(url_change_enrolment_status)

        response = self.app.put("/backstage-api/v1/party/change-enrolment-status", headers=self.headers,
                                data=json.dumps(self.enrolment_details))

        self.assertEqual(response.status_code, 200)

    def test_change_enrolment_status_bad_request(self):
        response = self.app.put("/backstage-api/v1/party/change-enrolment-status", headers=self.headers,
                                data=json.dumps({"bad": "Json"}))

        self.assertEqual(response.status_code, 400)

    @requests_mock.mock()
    def test_change_enrolment_status_fail(self, mock_request):
        mock_request.put(url_change_enrolment_status, status_code=500)

        response = self.app.put("/backstage-api/v1/party/change-enrolment-status", headers=self.headers,
                                data=json.dumps(self.enrolment_details))
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)
