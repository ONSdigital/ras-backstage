import json
import unittest

from flask import url_for
import requests_mock

from ras_backstage import app


url_upload_sample = f'{app.config["RM_SAMPLE_SERVICE"]}bres/fileupload'


class TestSample(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.csv_file = open('test/test_data/sample/business-survey-sample-date.csv', 'rb')

    @requests_mock.mock()
    def test_post_uploads_sample(self, mock_request):
        mock_request.post(url_upload_sample, json={'id': 'test-sample-id'}, status_code=201)
        upload_url = '/backstage-api/v1/sample/upload' \
                      '?collection_exercise_id=test-collex-id'

        response = self.app.post(
            upload_url, 
            data={'file': (self.csv_file, 'test.csv')})
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 201, response_data)
        self.assertEqual(response_data, 'test-sample-id')

    @requests_mock.mock()
    def test_post_sample_service_fails(self, mock_request):
        mock_request.post(url_upload_sample, status_code=500)
        upload_url = '/backstage-api/v1/sample/upload' \
                      '?collection_exercise_id=test-collex-id'

        response = self.app.post(
            upload_url, 
            data={'file': (self.csv_file, 'test.csv')})
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    def test_post_sample_missing(self):
        upload_url = '/backstage-api/v1/sample/upload' \
                      '?collection_exercise_id=test-collex-id'

        response = self.app.post(
            upload_url, 
            data={'file': None})
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)

    def test_post_sample_collex_id_missing(self):
        upload_url = '/backstage-api/v1/sample/upload'

        response = self.app.post(
            upload_url, 
            data={'file': (self.csv_file, 'test.csv')})
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
