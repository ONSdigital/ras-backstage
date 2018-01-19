import json
import unittest
from urllib.parse import urlencode

import requests_mock

from ras_backstage import app


url_get_survey_by_short_name = f'{app.config["RM_SURVEY_SERVICE"]}surveys/shortname/test'
url_ces = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
          'collectionexercises/survey/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87'
url_ce = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
         f'collectionexercises/e33daf0e-6a27-40cd-98dc-c6231f50e84a'
url_get_collection_instrument = f'{app.config["RAS_COLLECTION_INSTRUMENT_SERVICE"]}' \
                                   f'collection-instrument-api/1.0.2/collectioninstrument'
with open('test/test_data/collection_exercise/collection_exercise.json') as json_data:
    collection_exercise = json.load(json_data)


def _build_search_string():
    classifiers = {
        "SURVEY_ID": "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87",
        "COLLECTION_EXERCISE": "e33daf0e-6a27-40cd-98dc-c6231f50e84a"
    }
    return urlencode({'searchString': json.dumps(classifiers)})


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
    def test_single_collection_exercise(self, mock_request):
        # Given
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_ce, json=collection_exercise)
        search_string = _build_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}', json=self.collection_instruments,
                         complete_qs=True)

        # When
        response = self.app.get("/backstage-api/v1/collection-exercise/test/000000")
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['survey']['longName'],
                         'Business Register and Employment Survey')
        self.assertEqual(response_data['collection_exercise']['name'], '000000')

    @requests_mock.mock()
    def test_single_collection_exercise_survey_fail(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, status_code=500)

        response = self.app.get("/backstage-api/v1/collection-exercise/test/000000")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_single_collection_exercise_ce_fail(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, status_code=500)

        response = self.app.get("/backstage-api/v1/collection-exercise/test/000000")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_single_collection_exercise_ce_not_found(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=[])

        response = self.app.get("/backstage-api/v1/collection-exercise/test/000000")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['message'], 'Collection exercise not found')

    @requests_mock.mock()
    def test_single_collection_exercise_ces_fail(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_ce, status_code=500)

        response = self.app.get("/backstage-api/v1/collection-exercise/test/000000")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_collection_instrument(self, mock_request):
        # Given
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_ce, json=collection_exercise)
        search_string = _build_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}', json=self.collection_instruments,
                         complete_qs=True)

        # When
        response = self.app.get("/backstage-api/v1/collection-exercise/test/000000")
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['collection_instruments'], self.collection_instruments)

    @requests_mock.mock()
    def test_get_collection_instrument_returns_error(self, mock_request):
        # Given
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_ce, json=collection_exercise)
        search_string = _build_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}',
                         complete_qs=True, status_code=400)

        # When
        response = self.app.get('/backstage-api/v1/collection-exercise/test/000000')

        # Then
        self.assertEqual(response.status_code, 400)
