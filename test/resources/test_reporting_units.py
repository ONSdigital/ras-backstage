import json
import unittest

import requests_mock

from ras_backstage import app


url_search_businesses = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/businesses/search'
with open('test/test_data/party/reporting_unit_search.json') as json_data:
    business_search = json.load(json_data)
url_get_party_by_ru_ref = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/parties/type/B/ref/12345'
url_get_party_by_business_id = f'{app.config["RAS_PARTY_SERVICE"]}' \
                               f'party-api/v1/businesses/id/b3ba864b-7cbc-4f44-84fe-88dc018a1a4c'
with open('test/test_data/party/business_party.json') as json_data:
    party_business = json.load(json_data)
url_get_collection_exercises_by_party = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
                                       f'collectionexercises/party/b3ba864b-7cbc-4f44-84fe-88dc018a1a4c'
with open('test/test_data/collection_exercise/collection_exercise_list.json') as json_data:
    collection_exercise_list = json.load(json_data)
url_get_party_by_respondent_id = f'{app.config["RAS_PARTY_SERVICE"]}' \
                               f'party-api/v1/respondents/id/cd592e0f-8d07-407b-b75d-e01fbdae8233'
with open('test/test_data/party/business_party.json') as json_data:
    party_respondent = json.load(json_data)
url_get_cases_by_business_id = f'{app.config["RM_CASE_SERVICE"]}cases/partyid/b3ba864b-7cbc-4f44-84fe-88dc018a1a4c'
with open('test/test_data/case/case_list.json') as json_data:
    case_list = json.load(json_data)
url_get_survey_by_id = f'{app.config["RM_SURVEY_SERVICE"]}surveys/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87'
with open('test/test_data/survey/survey_list.json') as json_data:
    survey_list = json.load(json_data)
url_get_collection_exercise_by_survey = f'{app.config["RM_COLLECTION_EXERCISE_SERVICE"]}' \
                                        f'collectionexercises/survey/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef87'
with open('test/test_data/collection_exercise/collection_exercise.json') as json_data:
    collection_exercise = json.load(json_data)
url_get_iac_by_code = f'{app.config["RM_IAC_SERVICE"]}iacs/jkbvyklkwj88'
with open('test/test_data/iac_details.json') as json_data:
    iac_details = json.load(json_data)
url_get_case_groups_by_business_id = f'{app.config["RM_CASE_SERVICE"]}casegroups/partyid/b3ba864b-7cbc-4f44-84fe-88dc018a1a4c'
with open('test/test_data/case/case_groups.json') as json_data:
    case_group_list = json.load(json_data)


class TestReportingUnits(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @requests_mock.mock()
    def test_search_businesses(self, mock_request):
        mock_request.get(url_search_businesses, json=business_search)
        search_url = "/backstage-api/v1/reporting-unit/search?query=test"

        response = self.app.get(search_url)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)

    @requests_mock.mock()
    def test_search_businesses_fail(self, mock_request):
        mock_request.get(url_search_businesses, status_code=500)
        search_url = "/backstage-api/v1/reporting-unit/search?query=test"

        response = self.app.get(search_url)
        json.loads(response.data)

        self.assertEqual(response.status_code, 500)

    @requests_mock.mock()
    def test_get_reporting_unit(self, mock_request):
        mock_request.get(url_get_party_by_ru_ref, json=party_business)
        mock_request.get(url_get_collection_exercises_by_party, json=collection_exercise_list)
        mock_request.get(url_get_cases_by_business_id, json=case_list)
        mock_request.get(url_get_case_groups_by_business_id, json=case_group_list)
        mock_request.get(url_get_party_by_business_id, json=party_business)
        mock_request.get(url_get_survey_by_id, json=survey_list[0])
        mock_request.get(url_get_party_by_respondent_id, json=party_respondent)
        mock_request.get(url_get_iac_by_code, json=iac_details)

        response = self.app.get("/backstage-api/v1/reporting-unit/12345")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['surveys'][0]['surveyRef'], "221")
        self.assertEqual(response_data['surveys'][0]['collection_exercises'][0]['companyName'],
                         'Bolts and Ratchets Ltd')

    @requests_mock.mock()
    def test_get_reporting_unit_no_cases(self, mock_request):
        mock_request.get(url_get_party_by_ru_ref, json=party_business)
        mock_request.get(url_get_collection_exercises_by_party, json=collection_exercise_list)
        mock_request.get(url_get_cases_by_business_id, status_code=404)
        mock_request.get(url_get_case_groups_by_business_id, json=case_group_list)
        mock_request.get(url_get_party_by_business_id, json=party_business)
        mock_request.get(url_get_survey_by_id, json=survey_list[0])
        mock_request.get(url_get_party_by_respondent_id, json=party_respondent)

        response = self.app.get("/backstage-api/v1/reporting-unit/12345")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['surveys'][0]['surveyRef'], "221")

    @requests_mock.mock()
    def test_get_reporting_unit_no_collection_exercises(self, mock_request):
        mock_request.get(url_get_party_by_ru_ref, json=party_business)
        mock_request.get(url_get_collection_exercises_by_party, status_code=204)
        mock_request.get(url_get_cases_by_business_id, json=case_list)
        mock_request.get(url_get_case_groups_by_business_id, json=case_group_list)
        mock_request.get(url_get_party_by_business_id, json=party_business)
        mock_request.get(url_get_survey_by_id, json=survey_list[0])
        mock_request.get(url_get_party_by_respondent_id, json=party_respondent)

        response = self.app.get("/backstage-api/v1/reporting-unit/12345")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('surveys'), [])

    @requests_mock.mock()
    def test_get_reporting_unit_party_ru_fail(self, mock_request):
        mock_request.get(url_get_party_by_ru_ref, status_code=500)

        response = self.app.get("/backstage-api/v1/reporting-unit/12345")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_reporting_unit_collection_exercise_fail(self, mock_request):
        mock_request.get(url_get_party_by_ru_ref, json=party_business)
        mock_request.get(url_get_collection_exercises_by_party, status_code=500)

        response = self.app.get("/backstage-api/v1/reporting-unit/12345")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_reporting_unit_cases_fail(self, mock_request):
        mock_request.get(url_get_party_by_ru_ref, json=party_business)
        mock_request.get(url_get_collection_exercises_by_party, json=collection_exercise_list)
        mock_request.get(url_get_case_groups_by_business_id, json=case_group_list)
        mock_request.get(url_get_party_by_business_id, json=party_business)
        mock_request.get(url_get_survey_by_id, json=survey_list[0])
        mock_request.get(url_get_party_by_respondent_id, json=party_respondent)
        mock_request.get(url_get_cases_by_business_id, status_code=500)

        response = self.app.get("/backstage-api/v1/reporting-unit/12345")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_reporting_unit_business_party_id_fail(self, mock_request):
        mock_request.get(url_get_party_by_ru_ref, json=party_business)
        mock_request.get(url_get_collection_exercises_by_party, json=collection_exercise_list)
        mock_request.get(url_get_cases_by_business_id, json=case_list)
        mock_request.get(url_get_case_groups_by_business_id, json=case_group_list)
        mock_request.get(url_get_party_by_business_id, status_code=500)

        response = self.app.get("/backstage-api/v1/reporting-unit/12345")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_reporting_unit_survey_fail(self, mock_request):
        mock_request.get(url_get_party_by_ru_ref, json=party_business)
        mock_request.get(url_get_collection_exercises_by_party, json=collection_exercise_list)
        mock_request.get(url_get_cases_by_business_id, json=case_list)
        mock_request.get(url_get_case_groups_by_business_id, json=case_group_list)
        mock_request.get(url_get_party_by_business_id, json=party_business)
        mock_request.get(url_get_survey_by_id, status_code=500)

        response = self.app.get("/backstage-api/v1/reporting-unit/12345")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_reporting_unit_party_id_fail(self, mock_request):
        mock_request.get(url_get_party_by_ru_ref, json=party_business)
        mock_request.get(url_get_collection_exercises_by_party, json=collection_exercise_list)
        mock_request.get(url_get_cases_by_business_id, json=case_list)
        mock_request.get(url_get_case_groups_by_business_id, json=case_group_list)
        mock_request.get(url_get_party_by_business_id, json=party_business)
        mock_request.get(url_get_survey_by_id, json=survey_list[0])
        mock_request.get(url_get_party_by_respondent_id, status_code=500)

        response = self.app.get("/backstage-api/v1/reporting-unit/12345")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)

    @requests_mock.mock()
    def test_get_reporting_unit_iac_fail(self, mock_request):
        mock_request.get(url_get_party_by_ru_ref, json=party_business)
        mock_request.get(url_get_collection_exercises_by_party, json=collection_exercise_list)
        mock_request.get(url_get_cases_by_business_id, json=case_list)
        mock_request.get(url_get_case_groups_by_business_id, json=case_group_list)
        mock_request.get(url_get_party_by_business_id, json=party_business)
        mock_request.get(url_get_survey_by_id, json=survey_list[0])
        mock_request.get(url_get_party_by_respondent_id, json=party_respondent)
        mock_request.get(url_get_iac_by_code, status_code=500)

        response = self.app.get("/backstage-api/v1/reporting-unit/12345")
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response_data['error']['status_code'], 500)
