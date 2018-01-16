import json
import unittest
from io import BytesIO
from urllib.parse import urlencode

import requests_mock

from ras_backstage import app

url_get_survey_by_short_name = f'{app.config["RM_SURVEY_SERVICE"]}surveys/shortname/test'
url_ces = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
          'collectionexercises/survey/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87'
url_upload_collection_instrument = f'{app.config["RAS_COLLECTION_INSTRUMENT_SERVICE"]}' \
                                   f'collection-instrument-api/1.0.2/upload/e33daf0e-6a27-40cd-98dc-c6231f50e84a'
url_get_collection_instrument = f'{app.config["RAS_COLLECTION_INSTRUMENT_SERVICE"]}' \
                                   f'collection-instrument-api/1.0.2/collectioninstrument'


class TestCollectionExercise(unittest.TestCase):

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
                "exerciseRef": "201601",
                "scheduledExecutionDateTime": "2017-05-15T00:00:00Z"
            },
            {
                "id": "e33daf0e-6a27-40cd-98dc-c6231f50e84a",
                "exerciseRef": "000000",
                "scheduledExecutionDateTime": "2017-08-12T00:00:00Z"
            }
        ]
        self.collection_instruments = [
            {
                "classifiers": {
                    "COLLECTION_EXERCISE": [
                        "e33daf0e-6a27-40cd-98dc-c6231f50e84a"
                    ],
                    "RU_REF": [],
                    "SURVEY_ID": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87"
                },
                "file_name": "file",
                "id": "f732afbe-c710-4c95-a8d3-6644833195a7",
                "surveyId": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87"
            }
        ]

    @requests_mock.mock()
    def test_upload_collection_instrument(self, mock_request):
        classifiers = {
            "SURVEY_ID": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87",
            "COLLECTION_EXERCISE": "e33daf0e-6a27-40cd-98dc-c6231f50e84a"
        }
        params = urlencode({'classifiers': json.dumps(classifiers)})
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.post(f'{url_upload_collection_instrument}?{params}')

        response = self.app.post('/backstage-api/v1/collection-instrument/test/000000', data=dict(
            file=(BytesIO(b'data'), 'test.xlsx')))

        self.assertEqual(response.status_code, 201)

    @requests_mock.mock()
    def test_no_collection_instrument_file_uploaded(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.post(url_upload_collection_instrument)

        response = self.app.post('/backstage-api/v1/collection-instrument/test/000000')

        self.assertEqual(response.status_code, 400)

    @requests_mock.mock()
    def test_collection_exercise_period_does_not_match(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.post(url_upload_collection_instrument)

        response = self.app.post('/backstage-api/v1/collection-instrument/test/000001')

        self.assertEqual(response.status_code, 404)

    @requests_mock.mock()
    def test_get_collection_instrument(self, mock_request):
        # Given
        classifiers = {
            "SURVEY_ID": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87",
            "COLLECTION_EXERCISE": "e33daf0e-6a27-40cd-98dc-c6231f50e84a"
        }
        params = urlencode({'searchString': json.dumps(classifiers)})
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(f'{url_get_collection_instrument}?{params}', json=self.collection_instruments)

        # When
        response = self.app.get('/backstage-api/v1/collection-instrument/test/000000')

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), self.collection_instruments)

    @requests_mock.mock()
    def test_get_collection_instrument_returns_error(self, mock_request):
        # Given
        classifiers = {
            "SURVEY_ID": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87",
            "COLLECTION_EXERCISE": "e33daf0e-6a27-40cd-98dc-c6231f50e84a"
        }
        params = urlencode({'searchString': json.dumps(classifiers)})
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(f'{url_get_collection_instrument}?{params}', status_code=400)

        # When
        response = self.app.get('/backstage-api/v1/collection-instrument/test/000000')

        # Then
        self.assertEqual(response.status_code, 400)
