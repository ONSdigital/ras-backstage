import json
import unittest

import requests_mock

from ras_backstage import app


url_get_survey_list = '{}{}'.format(app.config['RAS_SURVEY_SERVICE'], 'surveys')
with open('test/test_data/survey/survey_list.json') as json_data:
    survey_list = json.load(json_data)


class TestSurvey(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @requests_mock.mock()
    def test_get_survey_list(self, mock_request):
        mock_request.get(url_get_survey_list, json=survey_list)

        response = self.app.get('/backstage-api/v1/survey/surveys')

        self.assertEqual(response.status_code, 200)
        self.assertIn('BRES'.encode(), response.data)
        self.assertIn('BRUS'.encode(), response.data)

    @requests_mock.mock()
    def test_get_survey_list_fail(self, mock_request):
        mock_request.get(url_get_survey_list, status_code=500)

        response = self.app.get('/backstage-api/v1/survey/surveys')

        self.assertEqual(response.status_code, 500)
        self.assertIn('"status_code": 500'.encode(), response.data)
