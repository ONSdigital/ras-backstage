import json
import unittest

import requests_mock

from ras_backstage import app


url_generate_new_code = f'{app.config["RM_CASE_SERVICE"]}cases/iac/ce_id/ru_ref'
with open('test/test_data/case/case_list.json') as json_data:
    case = json.load(json_data)[0]


class TestReportingUnitsGenerateNewCode(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @requests_mock.mock()
    def test_generate_new_code(self, mock_request):
        mock_request.post(url_generate_new_code, json=case)

        response = self.app.post("/backstage-api/v1/reporting-unit/iac/ce_id/ru_ref")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["iac"], "jkbvyklkwj88")

    @requests_mock.mock()
    def test_generate_new_code_fail(self, mock_request):
        mock_request.post(url_generate_new_code, json=case, status_code=500)

        response = self.app.post("/backstage-api/v1/reporting-unit/iac/ce_id/ru_ref")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)
