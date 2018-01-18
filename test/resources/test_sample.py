import json
import unittest

import requests_mock

from ras_backstage import app


url_get_survey_by_short_name = f'{app.config["RM_SURVEY_SERVICE"]}surveys/shortname/test'
url_ces = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
          'collectionexercises/survey/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87'
url_upload_sample = f'{app.config["RM_SAMPLE_SERVICE"]}samples/b/fileupload'


class TestSample(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.csv_file = open('test/test_data/sample/business-survey-sample-date.csv', 'rb')
        self.survey = {
            "id": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87",
            "longName": "Business Register and Employment Survey",
            "shortName": "BRES",
            "surveyRef": "221"
        }
        self.collection_exercises = [
          {
            "id": "c6467711-21eb-4e78-804c-1db8392f93fb",
            "exerciseRef": "201601",
            "scheduledExecutionDateTime": "2017-05-15T00:00:00Z"
          },
          {
            "id": "e33daf0e-6a27-40cd-98dc-c6231f50e84a",
            "exerciseRef": "000000",
            "scheduledExecutionDateTime": "2017-08-12T00:00:00Z"
          }
        ]

    @requests_mock.mock()
    def test_post_uploads_sample(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.post(url_upload_sample, json={'id': 'test-sample-id'}, status_code=201)

        response = self.app.post(
            '/backstage-api/v1/sample/test/000000',
            data={'file': (self.csv_file, 'test.csv')})
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['id'], 'test-sample-id')

    @requests_mock.mock()
    def test_post_sample_service_fails(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.post(url_upload_sample, status_code=500)

        response = self.app.post(
            '/backstage-api/v1/sample/test/000000',
            data={'file': (self.csv_file, 'test.csv')})
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_post_sample_missing(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.post(url_upload_sample)

        response = self.app.post('/backstage-api/v1/sample/test/000000')

        self.assertEqual(response.status_code, 400)

    @requests_mock.mock()
    def test_no_collection_exercise(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.post(url_upload_sample)

        response = self.app.post('/backstage-api/v1/sample/test/000001')

        self.assertEqual(response.status_code, 404)
