import json
import unittest

import requests_mock

from ras_backstage import app


url_get_survey_list = f'{app.config["RM_SURVEY_SERVICE"]}surveys'
with open('test/test_data/survey/survey_list.json') as json_data:
    survey_list = json.load(json_data)
url_get_survey_by_short_name = f'{app.config["RM_SURVEY_SERVICE"]}surveys/shortname/bres'


class TestSurvey(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.survey = {
            "id": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87",
            "longName": "Business Register and Employment Survey",
            "shortName": "BRES",
            "surveyRef": "221"
        }

    @requests_mock.mock()
    def test_get_survey_list(self, mock_request):
        mock_request.get(url_get_survey_list, json=survey_list)

        response = self.app.get('/backstage-api/v1/survey/surveys')

        self.assertEqual(response.status_code, 200)
        self.assertIn('BRES'.encode(), response.data)
        self.assertIn('BRUS'.encode(), response.data)

    @requests_mock.mock()
    def test_get_survey_list_no_surveys(self, mock_request):
        mock_request.get(url_get_survey_list, status_code=204)

        response = self.app.get('/backstage-api/v1/survey/surveys')

        self.assertEqual(response.status_code, 200)
        self.assertIn('[]'.encode(), response.data)

    @requests_mock.mock()
    def test_get_survey_list_fail(self, mock_request):
        mock_request.get(url_get_survey_list, status_code=500)

        response = self.app.get('/backstage-api/v1/survey/surveys')

        self.assertEqual(response.status_code, 500)
        self.assertIn('"status_code": 500'.encode(), response.data)

    @requests_mock.mock()
    def test_get_survey_list_JSONDecodeError(self, mock_request):
        mock_request.get(url_get_survey_list, text="aaaa")

        response = self.app.get('/backstage-api/v1/survey/surveys')

        self.assertEqual(response.status_code, 500)
        self.assertIn('"json": "aaaa"'.encode(), response.data)
        self.assertIn('"message": "Expecting value"'.encode(), response.data)

    @requests_mock.mock()
    def test_get_survey_by_short_name(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)

        response = self.app.get('/backstage-api/v1/survey/shortname/bres')

        self.assertEqual(response.status_code, 200)
        self.assertIn('"id": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87"'.encode(), response.data)
        self.assertIn('"longName": "Business Register and Employment Survey"'.encode(),
                      response.data)

    @requests_mock.mock()
    def test_get_survey_by_short_name_fail(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, status_code=500)

        response = self.app.get('/backstage-api/v1/survey/shortname/bres')

        self.assertEqual(response.status_code, 500)
        self.assertIn('"status_code": 500'.encode(), response.data)
