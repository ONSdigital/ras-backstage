import json
import unittest

import requests_mock

from ras_backstage import app


url_get_business_party = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/businesses/id/testid'
with open('test/test_data/party/business_party.json') as json_data:
    business_party = json.load(json_data)
url_get_respondent_party = f'{app.config["RAS_PARTY_SERVICE"]}' \
                           f'party-api/v1/respondents/id/testid'
with open('test/test_data/party/respondent_party.json') as json_data:
    respondent_party = json.load(json_data)


class TestParty(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @requests_mock.mock()
    def test_get_party_details(self, mock_request):
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_respondent_party, json=respondent_party)
        message_url = "/backstage-api/v1/party/party-details" \
                      "?business_party_id=testid&respondent_party_id=testid"

        response = self.app.get(message_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"name": "Business Register and Employment'.encode() in response.data)
        self.assertTrue('"partyId": "1216a88f-ee2a-420c-9e6a-ee34893c29c'.encode() in response.data)

    @requests_mock.mock()
    def test_get_party_details_business_fail(self, mock_request):
        mock_request.get(url_get_business_party, status_code=500)
        message_url = "/backstage-api/v1/party/party-details" \
                      "?business_party_id=testid&respondent_party_id=testid"

        response = self.app.get(message_url)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_get_party_details_respondent_fail(self, mock_request):
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_respondent_party, status_code=500)
        message_url = "/backstage-api/v1/party/party-details" \
                      "?business_party_id=testid&respondent_party_id=testid"

        response = self.app.get(message_url)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)
