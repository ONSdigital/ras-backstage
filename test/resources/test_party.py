import json
import unittest

import requests_mock

from ras_backstage import app

party_id = "cd592e0f-8d07-407b-b75d-e01fbdae8233"
url_get_business_party = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/businesses/id/testid'
url_get_reporting_unit = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/parties/type/B/ref/test_ru'
url_get_respondent_party_by_email = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/respondents/email'
url_search_businesses = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/businesses/search'
url_update_respondent_details = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/respondents/id/{party_id}'
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
        self.headers = {
            'Authorization': 'test_jwt',
            'Content-Type': 'application/json',
        }

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
        mock_request.put(url_update_respondent_details, status_code=200)
        url = f'/backstage-api/v1/party/update-respondent-details/{party_id}'
        response = self.app.put(url, headers=self.headers, data=json.dumps({
                                                      "first_name": 'John',
                                                      "last_name": 'Snow',
                                                      "telephone": '07437240752',
                                                      "email_address": 'old_address@example.com',
                                                      "new_email_address": 'new_address@example.com'}))

        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_update_respondent_details_fail(self, mock_request):
        mock_request.put(url_update_respondent_details, status_code=500)
        url = f'/backstage-api/v1/party/update-respondent-details/{party_id}'
        response = self.app.put(url, headers=self.headers, data=json.dumps({
                                                      "first_name": 'John',
                                                      "last_name": 'Snow',
                                                      "telephone": '07437240752',
                                                      "email_address": 'old_address@example.com',
                                                      "new_email_address": 'new_address@example.com'}))

        self.assertEqual(response.status_code, 500)

    @requests_mock.mock()
    def test_get_respondent_by_email_success(self, mock_request):
        mock_request.get(url_get_respondent_party_by_email, json=respondent_party, status_code=200)
        url = f'/backstage-api/v1/party/get-respondent-by-email'
        response = self.app.get(url, headers=self.headers, data=json.dumps({'email': "Jacky.Turner@email.com"}))
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['firstName'], 'Jacky')
        self.assertEqual(response_data['emailAddress'], 'Jacky.Turner@email.com')

    @requests_mock.mock()
    def test_get_respondent_by_email_no_respondent(self, mock_request):
        mock_request.get(url_get_respondent_party_by_email, status_code=404)
        url = f'/backstage-api/v1/party/get-respondent-by-email'
        response = self.app.get(url, headers=self.headers, data=json.dumps({'email': "Jacky.Turner@email.com"}))
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['Response'], 'No respondent found')

    @requests_mock.mock()
    def test_get_respondent_by_email_server_error(self, mock_request):
        mock_request.get(url_get_respondent_party_by_email, status_code=500)
        url = f'/backstage-api/v1/party/get-respondent-by-email'
        response = self.app.get(url, headers=self.headers, data=json.dumps({'email': "Jacky.Turner@email.com"}))

        self.assertEqual(response.status_code, 500)
