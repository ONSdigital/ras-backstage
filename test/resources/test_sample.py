import json
import unittest

import requests_mock

from ras_backstage import app


sample_summary_id = '08c191b8-e8b8-4920-b8de-87f85e536463'
collection_exercise_id = 'e33daf0e-6a27-40cd-98dc-c6231f50e84a'
survey_id = 'cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87'
test_period = '000000'
test_short_name = 'test'

url_get_survey_by_short_name = f'{app.config["RM_SURVEY_SERVICE"]}surveys/shortname/test'
url_ces = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
          f'collectionexercises/survey/{survey_id}'
url_sample_summary = f'{app.config["RM_SAMPLE_SERVICE"]}samples/samplesummary/{sample_summary_id}'
url_link_sample = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
                  f'collectionexercises/link/{collection_exercise_id}'


class TestSample(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.survey = {
            "id": survey_id,
            "longName": "Business Register and Employment Survey",
            "shortName": "test",
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
    def test_get_sample_summary(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_link_sample, json=[sample_summary_id])
        mock_request.get(url_sample_summary, json=self.sample_summary)

        response = self.app.get(f"/backstage-api/v1/sample/{test_short_name}/{test_period}")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, self.sample_summary)

    @requests_mock.mock()
    def test_get_collection_exercise_fails(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, status_code=500)

        response = self.app.get(f"/backstage-api/v1/sample/{test_short_name}/{test_period}")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_link_fails(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_link_sample, status_code=500)

        response = self.app.get(f"/backstage-api/v1/sample/{test_short_name}/{test_period}")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_sample_service_fails(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_link_sample, json=[sample_summary_id])
        mock_request.get(url_sample_summary, status_code=500)

        response = self.app.get(f"/backstage-api/v1/sample/{test_short_name}/{test_period}")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_link_empty_response(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_link_sample, json=[], status_code=204)

        response = self.app.get(f"/backstage-api/v1/sample/{test_short_name}/{test_period}")
        self.assertEqual(response.status_code, 204)

    @requests_mock.mock()
    def test_get_link_empty_list(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_link_sample, json=[])

        response = self.app.get(f"/backstage-api/v1/sample/{test_short_name}/{test_period}")
        self.assertEqual(response.status_code, 404)

    @requests_mock.mock()
    def test_get_no_linked_collection_exercise_found(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_link_sample, status_code=404)

        response = self.app.get(f"/backstage-api/v1/sample/{test_short_name}/{test_period}")
        self.assertEqual(response.status_code, 404)

    @requests_mock.mock()
    def test_get_no_summary_found(self, mock_request):
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_ces, json=self.collection_exercises)
        mock_request.get(url_link_sample, json=[sample_summary_id])
        mock_request.get(url_sample_summary, status_code=404)

        response = self.app.get(f"/backstage-api/v1/sample/{test_short_name}/{test_period}")
        self.assertEqual(response.status_code, 404)




    # @requests_mock.mock()
    # def test_no_collection_exercise_found(self, mock_request):
    #     mock_request.get(url_get_survey_by_short_name, json=self.survey)
    #     mock_request.get(url_ces, json={})
    #     mock_request.post(url_upload_sample)

    #     response = self.app.post(
    #         f"/backstage-api/v1/sample/test/000000",
    #         data={'file': (self.csv_file, 'test.csv')})

    #     self.assertEqual(response.status_code, 404)

    # @requests_mock.mock()
    # def test_collection_exercise_service_fails(self, mock_request):
    #     mock_request.get(url_get_survey_by_short_name, json=self.survey)
    #     mock_request.get(url_ces, status_code=500)
    #     mock_request.post(url_upload_sample)

    #     response = self.app.post(
    #         f"/backstage-api/v1/sample/test/000000",
    #         data={'file': (self.csv_file, 'test.csv')})

    #     self.assertEqual(response.status_code, 500)

    # @requests_mock.mock()
    # def test_link_sample_fails(self, mock_request):
    #     mock_request.get(url_get_survey_by_short_name, json=self.survey)
    #     mock_request.get(url_ces, json=self.collection_exercises)
    #     mock_request.post(url_upload_sample, json=self.sample_summary, status_code=201)
    #     mock_request.put(url_link_sample, status_code=500)

    #     response = self.app.post(
    #         f"/backstage-api/v1/sample/test/000000",
    #         data={'file': (self.csv_file, 'test.csv')})

    #     self.assertEqual(response.status_code, 500)

    # @requests_mock.mock()
    # def test_link_sample_fails_to_find_exercise(self, mock_request):
    #     mock_request.get(url_get_survey_by_short_name, json=self.survey)
    #     mock_request.get(url_ces, json=self.collection_exercises)
    #     mock_request.post(url_upload_sample, json=self.sample_summary, status_code=201)
    #     mock_request.put(url_link_sample, status_code=404)

    #     response = self.app.post(
    #         f"/backstage-api/v1/sample/test/000000",
    #         data={'file': (self.csv_file, 'test.csv')})

    #     self.assertEqual(response.status_code, 404)
