import json
import unittest

from requests.exceptions import RequestException
import requests_mock

from ras_backstage import app

surveyRef = '023'
survey_ref = '023'

url_get_survey_list = f'{app.config["RM_SURVEY_SERVICE"]}surveys'
with open('test/test_data/survey/survey_list.json') as json_data:
    survey_list = json.load(json_data)
url_get_survey_by_short_name = f'{app.config["RM_SURVEY_SERVICE"]}surveys/shortname/bres'
url_get_collection_exercises = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
                               'collectionexercises/survey/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87'
url_update_survey_details = f'{app.config["RM_SURVEY_SERVICE"]}surveys/ref/{surveyRef}'
url_get_collection_exercise_events = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
                                'collectionexercises/c6467711-21eb-4e78-804c-1db8392f93fb/events'
url_get_collection_exercises_link = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
                                'collectionexercises/link/c6467711-21eb-4e78-804c-1db8392f93fb'
url_get_sample_summary = f'{app.config["RM_SAMPLE_SERVICE"]}' \
                            'samples/samplesummary/b9487b59-2ac7-4fbf-b734-5a4c260ff235'


class TestSurvey(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = {
            'Content-Type': 'application/json',
        }
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

        self.collection_exercises_events = [
            {
                "id": "b4a36392-a21f-485b-9dc4-d151a8fcd565",
                "collectionExerciseId": "92d436aa-1251-4ae3-bad1-f3ae950f87be",
                "tag": "mps",
                "timestamp": "2018-03-16T00:00:00.000Z"
            }
        ]

        self.collection_exercises_link = ["b9487b59-2ac7-4fbf-b734-5a4c260ff235"]

        self.sample_summary = {
            "id": "b9487b59-2ac7-4fbf-b734-5a4c260ff235",
            "effectiveStartDateTime": "",
            "effectiveEndDateTime": "",
            "surveyRef": "",
            "ingestDateTime": "2018-03-14T14:29:51.325Z",
            "state": "ACTIVE",
            "totalSampleUnits": 5,
            "expectedCollectionInstruments": 1
        }

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
        mock_request.get(url_get_collection_exercise_events, json=self.collection_exercises_events)
        mock_request.get(url_get_collection_exercises_link, json=self.collection_exercises_link)
        mock_request.get(url_get_sample_summary, json=self.sample_summary)

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

    @requests_mock.mock()
    def test_edit_survey_details_success(self, mock_request):
        mock_request.put(url_update_survey_details, status_code=200)
        url = f'backstage-api/v1/survey/edit-survey-details/{survey_ref}'
        response = self.app.put(url, headers=self.headers, data=json.dumps({
            "long_name": 'Survey Test Name',
            "short_name": 'QBZ'
        }))
        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_edit_survey_details_failure(self, mock_request):
        mock_request.put(url_update_survey_details, status_code=500)
        url = f'backstage-api/v1/survey/edit-survey-details/{survey_ref}'
        response = self.app.put(url, headers=self.headers, data=json.dumps({
            "long_name": 'Survey Test Name',
            "short_name": 'QBZ'
        }))
        self.assertEqual(response.status_code, 500)

    @requests_mock.mock()
    def test_edit_survey_details_not_found(self, mock_request):
        mock_request.put(url_update_survey_details, status_code=404)
        url = f'backstage-api/v1/survey/edit-survey-details/{survey_ref}'
        response = self.app.put(url, headers=self.headers, data=json.dumps({
            "long_name": 'Survey Test Name',
            "short_name": 'QBZ'
        }))
        self.assertEqual(response.status_code, 404)

    @requests_mock.mock()
    def test_edit_survey_details_no_data(self, mock_request):
        mock_request.put(url_update_survey_details, status_code=404)
        url = f'backstage-api/v1/survey/edit-survey-details/{survey_ref}'
        response = self.app.put(url, headers=self.headers, data=json.dumps({
            "long_name": '',
            "short_name": ''
        }))
        self.assertEqual(response.status_code, 404)
