import json
import unittest

import requests_mock

from ras_backstage import app


url_search_businesses = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/businesses/search'
with open('test/test_data/party/reporting_unit_search.json') as json_data:
    business_search = json.load(json_data)


class TestReportingUnits(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @requests_mock.mock()
    def test_search_businesses(self, mock_request):
        mock_request.get(url_search_businesses, json=business_search)
        search_url = "/backstage-api/v1/reporting-unit/search?query=test"

        response = self.app.get(search_url)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)

    @requests_mock.mock()
    def test_search_businesses_fail(self, mock_request):
        mock_request.get(url_search_businesses, status_code=500)
        search_url = "/backstage-api/v1/reporting-unit/search?query=test"

        response = self.app.get(search_url)
        json.loads(response.data)

        self.assertEqual(response.status_code, 500)

    @requests_mock.mock()
    def test_search_businesses(self, mock_request):
        mock_request.get(url_search_businesses, json=business_search)
        search_url = "/backstage-api/v1/reporting-unit/search?query=test"

        response = self.app.get(search_url)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)
