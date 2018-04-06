import json
import unittest

import requests_mock

from ras_backstage import app

survey_short_name = 'BRES'
period = '201801'
survey_id = 'cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87'
collection_exercise_id = '14fb3e68-4dca-46db-bf49-04b84e07e77c'

url_get_survey = f'{app.config["RM_SURVEY_SERVICE"]}surveys/shortname/{survey_short_name}'
with open('test/test_data/survey/survey_list.json') as json_data:
    survey = json.load(json_data)[0]
url_get_collection_exercises_for_survey = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}collectionexercises' \
                                          f'/survey/{survey_id}'
with open('test/test_data/collection_exercise/collection_exercise_list.json') as json_data:
    collection_exercise_list = json.load(json_data)
url_get_events = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}collectionexercises/{collection_exercise_id}/events'
with open('test/test_data/collection_exercise/collection_exercise_events.json') as json_data:
    events = json.load(json_data)
url_put_update_event = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}collectionexercises' \
                       f'/{collection_exercise_id}/events/go_live'


class TestUpdateEventDate(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = {
            'Content-Type': 'application/json',
        }

    @requests_mock.mock()
    def test_get_update_event_date(self, mock_request):
        # Given
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_exercises_for_survey, json=collection_exercise_list)
        mock_request.get(url_get_events, json=events)

        # When
        url = f'/backstage-api/v1/collection-exercise/{survey_short_name}/{period}/update-events'
        response = self.app.get(url)
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['collection_exercise']['id'], collection_exercise_id)
        self.assertEqual(response_data['survey']['id'], survey_id)
        self.assertEqual(response_data['events'][0]['tag'], 'mps')

    @requests_mock.mock()
    def test_get_update_event_date_no_ce(self, mock_request):
        # Given
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_exercises_for_survey, json=collection_exercise_list)
        mock_request.get(url_get_events, json=events)

        # When
        url = f'/backstage-api/v1/collection-exercise/{survey_short_name}/201813/update-events'
        response = self.app.get(url)
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['message'], "Collection exercise not found")

    @requests_mock.mock()
    def test_get_update_event_date_survey_fail(self, mock_request):
        # Given
        mock_request.get(url_get_survey, status_code=500)

        # When
        url = f'/backstage-api/v1/collection-exercise/{survey_short_name}/{period}/update-events'
        response = self.app.get(url)
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_update_event_date_exercises_fail(self, mock_request):
        # Given
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_exercises_for_survey, status_code=500)

        # When
        url = f'/backstage-api/v1/collection-exercise/{survey_short_name}/{period}/update-events'
        response = self.app.get(url)
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_update_event_date_events_fail(self, mock_request):
        # Given
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_exercises_for_survey, json=collection_exercise_list)
        mock_request.get(url_get_events, status_code=500)

        # When
        url = f'/backstage-api/v1/collection-exercise/{survey_short_name}/{period}/update-events'
        response = self.app.get(url)
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_put_update_event_date(self, mock_request):
        # Given
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_exercises_for_survey, json=collection_exercise_list)
        mock_request.put(url_put_update_event, status_code=201)

        # When
        url = f'/backstage-api/v1/collection-exercise/{survey_short_name}/{period}/update-events/go_live'
        response = self.app.put(url, headers=self.headers,
                                data=json.dumps({"timestamp": '2018-05-22T00:00:00.000+0000'}))

        # Then
        self.assertEqual(response.status_code, 201)

    @requests_mock.mock()
    def test_put_update_event_date_no_ce(self, mock_request):
        # Given
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_exercises_for_survey, json=collection_exercise_list)

        # When
        url = f'/backstage-api/v1/collection-exercise/{survey_short_name}/201813/update-events/go_live'
        response = self.app.put(url, headers=self.headers,
                                data=json.dumps({"timestamp": '2018-05-22T00:00:00.000+0000'}))
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data['message'], "Collection exercise not found")

    @requests_mock.mock()
    def test_put_update_event_date_fail(self, mock_request):
        # Given
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_exercises_for_survey, json=collection_exercise_list)
        mock_request.put(url_put_update_event, status_code=500)

        # When
        url = f'/backstage-api/v1/collection-exercise/{survey_short_name}/{period}/update-events/go_live'
        response = self.app.put(url, headers=self.headers,
                                data=json.dumps({"timestamp": '2018-05-22T00:00:00.000+0000'}))
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)
