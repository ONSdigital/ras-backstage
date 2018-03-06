import json
import unittest

import requests_mock

from ras_backstage import app


url_get_business_party = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/businesses/id/testid'
url_get_reporting_unit = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/parties/type/B/ref/test_ru'
url_search_businesses = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/businesses/search'
url_update_respondent_details = f'{app.config["RAS_PARTY_SERVICE"]}/party-api/v1/respondents/update_respondent_details'
with open('test/test_data/party/business_party.json') as json_data:
    business_party = json.load(json_data)
url_get_respondent_party = f'{app.config["RAS_PARTY_SERVICE"]}' \
                           f'party-api/v1/respondents/id/testid'
with open('test/test_data/party/respondent_party.json') as json_data:
    respondent_party = json.load(json_data)
with open('test/test_data/party/reporting_unit_search.json') as json_data:
    business_search = json.load(json_data)


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
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['business_party']['name'], "Bolts and Ratchets Ltd")
        self.assertIsNotNone(response_data['business_party']['associations'][0]['enrolments'][0])

    @requests_mock.mock()
    def test_get_party_details_business_fail(self, mock_request):
        mock_request.get(url_get_business_party, status_code=500)
        message_url = "/backstage-api/v1/party/party-details" \
                      "?business_party_id=testid&respondent_party_id=testid"

        response = self.app.get(message_url)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_party_details_respondent_fail(self, mock_request):
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_respondent_party, status_code=500)
        message_url = "/backstage-api/v1/party/party-details" \
                      "?business_party_id=testid&respondent_party_id=testid"

        response = self.app.get(message_url)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_update_respondent_details(self, mock_request):
        mock_request.get(url_get_respondent_party, json=respondent_party)
        url = '/backstage-api/v1/party/update-respondent-details'

        response = self.app.post(url, data=json.dumps({"firstName": 'John',
                                                      "lastName": 'Snow',
                                                      "telephone": '07837240752'}))
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["first_name"]["John"], 200)

    # @requests_mock.mock()
    # def test_update_respondent_details_fail(self, mock_request):
    #     mock_request.get(url_get_respondent_party, json=respondent_party)
    #     mock_request.put(url_update_respondent_details, status_code=500)
    #     url = '/backstage-api/v1/party/update_respondent_details'
    #
    #     response = self.app.put(url, data=json.dumps({}))
    #     response_data = json.loads(response.data)
    #
    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(response_data['error']['status_code'], 500)
