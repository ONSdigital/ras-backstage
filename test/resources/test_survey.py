import json
import unittest

from requests.exceptions import RequestException
import requests_mock

from ras_backstage import app


url_get_survey_list = f'{app.config["RM_SURVEY_SERVICE"]}surveys'
with open('test/test_data/survey/survey_list.json') as json_data:
    survey_list = json.load(json_data)
url_get_survey_by_short_name = f'{app.config["RM_SURVEY_SERVICE"]}surveys/shortname/bres'
url_get_collection_exercises = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
                               'collectionexercises/survey/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87'


class TestSurvey(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.survey = {
            "id": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87",
            "longName": "Business Register and Employment Survey",
            "shortName": "BRES",
            "surveyRef": "221"
        }
        self.collection_exercises = [
            {
                "id": "c6467711-21eb-4e78-804c-1db8392f93fb",
                "name": "201601",
                "scheduledExecutionDateTime": "2017-05-15T00:00:00Z"
            }
        ]

    @requests_mock.mock()
    def test_get_survey_list(self, mock_request):
        mock_request.get(url_get_survey_list, json=survey_list)

        response = self.app.get('/backstage-api/v1/survey/surveys')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data[0]['shortName'], "RSI")
        self.assertEqual(response_data[1]['shortName'], "MWSS")
        self.assertEqual(response_data[2]['shortName'], "BRES")

    @requests_mock.mock()
    def test_get_survey_list_no_surveys(self, mock_request):
        mock_request.get(url_get_survey_list, status_code=204)

        response = self.app.get('/backstage-api/v1/survey/surveys')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, [])

    @requests_mock.mock()
    def test_get_survey_list_fail(self, mock_request):
        mock_request.get(url_get_survey_list, status_code=500)

        response = self.app.get('/backstage-api/v1/survey/surveys')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_survey_list_JSONDecodeError(self, mock_request):
        mock_request.get(url_get_survey_list, text="aaaa")

        response = self.app.get('/backstage-api/v1/survey/surveys')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['json'], "aaaa")
        self.assertEqual(response_data['error']['message'], "Expecting value")

    @requests_mock.mock()
    def test_get_survey_by_short_name(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_get_collection_exercises, json=self.collection_exercises)

        response = self.app.get('/backstage-api/v1/survey/shortname/bres')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['collection_exercises'][0]['name'], "201601")
        self.assertEqual(response_data['collection_exercises'][0]['id'],
                         "c6467711-21eb-4e78-804c-1db8392f93fb")
        self.assertEqual(response_data['survey']['longName'],
                         "Business Register and Employment Survey")

    @requests_mock.mock()
    def test_get_survey_by_short_name_survey_connection_error(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, exc=RequestException)

        response = self.app.get('/backstage-api/v1/survey/shortname/bres')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_survey_by_short_name_survey_fail(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, status_code=500)

        response = self.app.get('/backstage-api/v1/survey/shortname/bres')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_survey_by_short_name_ce_fail(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_get_collection_exercises, status_code=500)

        response = self.app.get('/backstage-api/v1/survey/shortname/bres')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_survey_by_short_name_ce_empty(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_get_collection_exercises, status_code=204)

        response = self.app.get('/backstage-api/v1/survey/shortname/bres')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['collection_exercises'], [])
        self.assertEqual(response_data['survey']['id'], "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87")
