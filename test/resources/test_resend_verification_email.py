import unittest
import requests_mock

from ras_backstage import app

url_resend_verification_email = app.config['RAS_PARTY_RESEND_VERIFICATION_EMAIL'].format('test_party_id')


class TestResendVerificationEmail(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.valid_response = {"message": "A new verification email has been sent"}
        self.invalid_party_response = {"message": "There is no respondent with that party ID "}

    @requests_mock.mock()
    def test_resend_verification_email(self, mock_request):
        mock_request.get(url_resend_verification_email, status_code=200, json=self.valid_response)

        response = self.app.post('/backstage-api/v1/reporting-unit/resend-verification-email/test_party_id')

        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_resend_verification_email_fail_no_party(self, mock_request):
        mock_request.get(url_resend_verification_email, status_code=404, json=self.invalid_party_response)

        response = self.app.post('/backstage-api/v1/reporting-unit/resend-verification-email/test_party_id')

        self.assertEqual(response.status_code, 404)
        self.assertTrue('"status_code": 404'.encode() in response.data)

    @requests_mock.mock()
    def test_resend_verification_email_fail_notification_error(self, mock_request):
        mock_request.get(url_resend_verification_email, status_code=500)

        response = self.app.post('/backstage-api/v1/reporting-unit/resend-verification-email/test_party_id')

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)
