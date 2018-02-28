import json
import unittest

import requests_mock

from ras_backstage import app
from ras_backstage.controllers.case_controller import filter_statuses

url_get_party_by_ru_ref = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/parties/type/B/ref/12345'
with open('test/test_data/party/business_party.json') as json_data:
    party_business = json.load(json_data)

url_get_cases_by_business_id = f'{app.config["RM_CASE_SERVICE"]}cases/partyid/b3ba864b-7cbc-4f44-84fe-88dc018a1a4c'
with open('test/test_data/case/case_list.json') as json_data:
    case_list = json.load(json_data)

url_get_statuses_for_ru_ref = f'{app.config["RM_CASE_SERVICE"]}' \
                              f'casegroups/transitions/14fb3e68-4dca-46db-bf49-04b84e07e77c/12345'
url_update_status_for_ru_ref = f'{app.config["RM_CASE_SERVICE"]}' \
                              f'casegroups/transitions/14fb3e68-4dca-46db-bf49-04b84e07e77c/12345'

url_get_survey_by_short_name = f'{app.config["RM_SURVEY_SERVICE"]}surveys/shortname/BRES'

url_get_collection_exercises_by_survey = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
                                        f'collectionexercises/survey/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87'
with open('test/test_data/collection_exercise/collection_exercise_list.json') as json_data:
    collection_exercises = json.load(json_data)


class TestReportingUnits(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.survey = {
            "id": 'cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87',
            "longName": "Business Register and Employment Survey",
            "shortName": "BRES",
            "surveyRef": "221"
        }
        self.statuses = {
            "UPLOADED": "COMPLETE",
            "COMPLETEDBYPHONE": "COMPLETEDBYPHONE"
        }

    @requests_mock.mock()
    def test_get_reporting_unit_statuses(self, mock_request):
        # Given
        mock_request.get(url_get_party_by_ru_ref, json=party_business)
        mock_request.get(url_get_cases_by_business_id, json=case_list)
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_get_collection_exercises_by_survey, json=collection_exercises)
        self.statuses = {
            "UPLOADED": "COMPLETE",
            "COMPLETEDBYPHONE": "COMPLETEDBYPHONE"
        }
        mock_request.get(url_get_statuses_for_ru_ref, json=self.statuses)

        # When
        response = self.app.get("/backstage-api/v1/case/status/BRES/201801/12345")
        response_data = json.loads(response.data)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['current_status'], 'NOTSTARTED')
        self.assertEqual(response_data['available_statuses']['COMPLETEDBYPHONE'], "COMPLETEDBYPHONE")

    @requests_mock.mock()
    def test_get_reporting_unit_statuses_fail(self, mock_request):
        # Given
        mock_request.get(url_get_party_by_ru_ref, json=party_business)
        mock_request.get(url_get_cases_by_business_id, json=case_list)
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_get_collection_exercises_by_survey, json=collection_exercises)
        mock_request.get(url_get_statuses_for_ru_ref, status_code=500)

        response = self.app.get("/backstage-api/v1/case/status/BRES/201801/12345")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_should_update_status_to_completed_by_phone(self, mock_request):
        # Given
        mock_request.get(url_get_party_by_ru_ref, json=party_business)
        mock_request.get(url_get_cases_by_business_id, json=case_list)
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_get_collection_exercises_by_survey, json=collection_exercises)
        mock_request.put(url_update_status_for_ru_ref,
                         additional_matcher=lambda r: {'event': 'COMPLETEDBYPHONE'} == r.json())

        # When
        response = self.app.post("/backstage-api/v1/case/status/BRES/201801/12345",
                                 data=json.dumps({'event': 'COMPLETEDBYPHONE'}), content_type='application/json')

        # Then
        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_should_return_api_error_code_when_update_status_fails(self, mock_request):
        # Given
        mock_request.get(url_get_party_by_ru_ref, json=party_business)
        mock_request.get(url_get_cases_by_business_id, json=case_list)
        mock_request.get(url_get_survey_by_short_name, json=self.survey)
        mock_request.get(url_get_collection_exercises_by_survey, json=collection_exercises)
        mock_request.put(url_update_status_for_ru_ref, status_code=503)

        # When
        response = self.app.post("/backstage-api/v1/case/status/BRES/201801/12345",
                                 data=json.dumps({'event': 'COMPLETEDBYPHONE'}), content_type='application/json')

        # Then
        self.assertEqual(response.status_code, 503)

    def test_should_return_400_when_event_not_posted(self):
        # Given
        body = {}

        # When
        response = self.app.post("/backstage-api/v1/case/status/BRES/201801/12345",
                                 data=json.dumps(body), content_type='application/json')

        # Then
        self.assertEqual(response.status_code, 400)


    @requests_mock.mock()
    def test_filter_other_options_when_not_started(self, mock_request):
        # Given
        current_status = 'INPROGRESS'
        statuses = {
            'UPLOAD': 'COMPLETED',
            'COMPLETEDBYPHONE': 'COMPLETEDBYPHONE',
            'SOMETHING': 'SOMETHING',
        }

        # When
        filtered_statuses = filter_statuses(current_status, statuses)

        # Then
        self.assertEqual(filtered_statuses['COMPLETEDBYPHONE'], 'COMPLETEDBYPHONE')
        self.assertNotIn('COMPLETED', filtered_statuses.values())
        self.assertNotIn('SOMETHING', filtered_statuses.values())

    @requests_mock.mock()
    def test_filter_other_options_when_in_progress(self, mock_request):
        # Given
        current_status = 'INPROGRESS'
        statuses = {
            'UPLOAD': 'COMPLETED',
            'COMPLETEDBYPHONE': 'COMPLETEDBYPHONE',
            'SOMETHING': 'SOMETHING',
        }

        # When
        filtered_statuses = filter_statuses(current_status, statuses)

        # Then
        self.assertEqual(filtered_statuses['COMPLETEDBYPHONE'], 'COMPLETEDBYPHONE')
        self.assertNotIn('COMPLETED', filtered_statuses.values())
        self.assertNotIn('SOMETHING', filtered_statuses.values())

    @requests_mock.mock()
    def test_filter_other_options_when_reopened(self, mock_request):
        # Given
        current_status = 'REOPENED'
        statuses = {
            'UPLOAD': 'COMPLETED',
            'COMPLETEDBYPHONE': 'COMPLETEDBYPHONE',
            'SOMETHING': 'SOMETHING',
        }

        # When
        filtered_statuses = filter_statuses(current_status, statuses)

        # Then
        self.assertEqual(filtered_statuses['COMPLETEDBYPHONE'], 'COMPLETEDBYPHONE')
        self.assertNotIn('COMPLETED', filtered_statuses.values())
        self.assertNotIn('SOMETHING', filtered_statuses.values())