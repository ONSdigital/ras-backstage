import json
import unittest
from urllib.parse import urlencode

import requests_mock

from ras_backstage import app


collection_exercise_id = 'e33daf0e-6a27-40cd-98dc-c6231f50e84a'
collection_instrument_id = 'f732afbe-c710-4c95-a8d3-6644833195a7'
sample_summary_id = '08c191b8-e8b8-4920-b8de-87f85e536463'
survey_id = 'cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87'
test_period = '000000'
test_short_name = 'test'

url_sample_summary = f'{app.config["RM_SAMPLE_SERVICE"]}samples/samplesummary/{sample_summary_id}'
url_link_sample = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
                  f'collectionexercises/link/{collection_exercise_id}'
url_get_survey_by_short_name = f'{app.config["RM_SURVEY_SERVICE"]}surveys/shortname/test'
url_ces = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
          f'collectionexercises/survey/{survey_id}'
url_ce = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
         f'collectionexercises/{collection_exercise_id}'
url_ce_execute = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
         f'collectionexerciseexecution/{collection_exercise_id}'
url_get_collection_instrument = f'{app.config["RAS_COLLECTION_INSTRUMENT_SERVICE"]}' \
                                   f'collection-instrument-api/1.0.2/collectioninstrument'

with open('test/test_data/collection_exercise/collection_exercise.json') as json_data:
    collection_exercise = json.load(json_data)
url_ce_events = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
                f'collectionexercises/e33daf0e-6a27-40cd-98dc-c6231f50e84a/events'
with open('test/test_data/collection_exercise/collection_exercise_events.json') as json_data:
    events = json.load(json_data)


def _build_search_string():
    classifiers = {
        "SURVEY_ID": survey_id,
        "COLLECTION_EXERCISE": collection_exercise_id
    }
    return urlencode({'searchString': json.dumps(classifiers)})


def _build_ci_type_search_string():
    classifiers = {
        "SURVEY_ID": survey_id,
        "TYPE": "EQ"
    }
    return urlencode({'searchString': json.dumps(classifiers)})


class TestCollectionExercise(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.survey = {
            "id": survey_id,
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
            "id": collection_exercise_id,
            "exerciseRef": test_period,
            "scheduledExecutionDateTime": "2017-08-12T00:00:00Z"
          }
        ]
        self.collection_instruments = [
            {
                "classifiers": {
                    "COLLECTION_EXERCISE": [
                        collection_exercise_id,
                    ],
                    "RU_REF": [],
                    "SURVEY_ID": survey_id,
                },
                "file_name": "file",
                "id": collection_instrument_id,
                "surveyId": survey_id
            }
        ]
        self.eq_ci_selectors = [
            {
                "classifiers": {
                    "COLLECTION_EXERCISE": [
                    ],
                    "RU_REF": [],
                    "SURVEY_ID": survey_id,
                },
                "file_name": None,
                "id": collection_instrument_id,
                "surveyId": survey_id
            }
        ]
        self.sample_summary = {
            "sampleSummaryPK": 1,
            "id": sample_summary_id,
            "state": "INIT",
            "ingestDateTime": "2017-11-06T14:02:24.203+0000"
        }
        self.linked_sample = {
            "collectionExerciseId": collection_exercise_id,
            "sampleSummaryIds": [
                sample_summary_id,
            ]
        }

    @requests_mock.mock()
    def test_single_collection_exercise(self, mock_request):
        # Given
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_ce, json=collection_exercise)
        mock_request.get(url_ce_events, json=events)
        mock_request.get(url_link_sample, json=[sample_summary_id])
        mock_request.get(url_sample_summary, json=self.sample_summary)
        search_string = _build_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}', json=self.collection_instruments,
                         complete_qs=True)
        search_string = _build_ci_type_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}', json=self.collection_instruments,
                         complete_qs=True)

        # When
        response = self.app.get(f'/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}')
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['survey']['longName'],
                         'Business Register and Employment Survey')
        self.assertEqual(response_data['collection_exercise']['name'], '000000')
        self.assertEqual(response_data['events'][0]['tag'], "mps")
        self.assertEqual(response_data['eq_ci_selectors'], self.collection_instruments)

    @requests_mock.mock()
    def test_single_collection_exercise_survey_fail(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, status_code=500)

        response = self.app.get(f"/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_single_collection_exercise_ce_fail(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, status_code=500)

        response = self.app.get(f"/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_single_collection_exercise_ce_not_found(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=[])

        response = self.app.get(f"/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['message'], 'Collection exercise not found')

    @requests_mock.mock()
    def test_single_collection_exercise_ces_fail(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_ce, status_code=500)

        response = self.app.get(f"/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_single_collection_exercise_ce_events_fail(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_ce, json=collection_exercise)
        mock_request.get(url_ce_events, status_code=500)

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
        mock_request.get(url_ce_events, json=events)
        mock_request.get(url_link_sample, json=[sample_summary_id])
        mock_request.get(url_sample_summary, json=self.sample_summary)
        search_string = _build_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}', json=self.collection_instruments,
                         complete_qs=True)
        search_string = _build_ci_type_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}', json=self.collection_instruments,
                         complete_qs=True)

        # When
        response = self.app.get(f"/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}")
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
        mock_request.get(url_ce_events, json=events)
        search_string = _build_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}',
                         complete_qs=True, status_code=400)
        search_string = _build_ci_type_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}', json=self.collection_instruments,
                         complete_qs=True)

        # When
        response = self.app.get(f'/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}')

        # Then
        self.assertEqual(response.status_code, 400)

    @requests_mock.mock()
    def test_get_sample_summary(self, mock_request):
        # Given
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_ce, json=collection_exercise)
        mock_request.get(url_ce_events, json=events)
        mock_request.get(url_link_sample, json=[sample_summary_id])
        mock_request.get(url_sample_summary, json=self.sample_summary)
        search_string = _build_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}', json=self.collection_instruments,
                         complete_qs=True)
        search_string = _build_ci_type_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}', json=self.collection_instruments,
                         complete_qs=True)

        # When
        response = self.app.get(f"/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}")
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['sample_summary'], self.sample_summary)

    @requests_mock.mock()
    def test_get_no_linked_summaries(self, mock_request):
        # Given
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_ce, json=collection_exercise)
        mock_request.get(url_ce_events, json=events)
        search_string = _build_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}', json=self.collection_instruments,
                         complete_qs=True)
        search_string = _build_ci_type_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}', json=self.collection_instruments,
                         complete_qs=True)
        mock_request.get(url_link_sample, status_code=204)

        # When
        response = self.app.get(f'/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}')
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['sample_summary'], None)

    @requests_mock.mock()
    def test_get_link_returns_error(self, mock_request):
        # Given
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_ce, json=collection_exercise)
        mock_request.get(url_ce_events, json=events)
        mock_request.get(url_link_sample, status_code=400)
        search_string = _build_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}', json=self.collection_instruments,
                         complete_qs=True)
        search_string = _build_ci_type_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}', json=self.collection_instruments,
                         complete_qs=True)

        # When
        response = self.app.get(f'/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}')

        # Then
        self.assertEqual(response.status_code, 400)

    @requests_mock.mock()
    def test_get_sample_returns_error(self, mock_request):
        # Given
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_ce, json=collection_exercise)
        mock_request.get(url_ce_events, json=events)
        mock_request.get(url_link_sample, json=[sample_summary_id])
        mock_request.get(url_sample_summary, status_code=400)
        search_string = _build_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}', json=self.collection_instruments,
                         complete_qs=True)
        search_string = _build_ci_type_search_string()
        mock_request.get(f'{url_get_collection_instrument}?{search_string}', json=self.collection_instruments,
                         complete_qs=True)

        # When
        response = self.app.get(f'/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}')

        # Then
        self.assertEqual(response.status_code, 400)

    @requests_mock.mock()
    def test_execute_collection_exercise(self, mock_request):
        # Given
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.post(url_ce_execute, status_code=200)

        # When
        response = self.app.post(f'/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}/execute')

        # Then
        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_execute_collection_exercise_not_found(self, mock_request):
        # Given
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=[])

        # When
        response = self.app.post(f'/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}/execute')
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['message'], 'Collection exercise not found')

    @requests_mock.mock()
    def test_execute_collection_exercise_survey_fails(self, mock_request):
        # Given
        mock_request.get(url_get_survey_by_short_name, status_code=500)

        # When
        response = self.app.post(f'/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}/execute')
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_execute_collection_exercise_ces_fails(self, mock_request):
        # Given
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, status_code=500)

        # When
        response = self.app.post(f'/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}/execute')
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_execute_collection_exercise_ce_fails(self, mock_request):
        # Given
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.post(url_ce_execute, status_code=500)

        # When
        response = self.app.post(f'/backstage-api/v1/collection-exercise/{test_short_name}/{test_period}/execute')
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)
