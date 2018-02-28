import unittest
import logging

from werkzeug.exceptions import InternalServerError

from ras_backstage import app
from ras_backstage.authentication.token_decoder import decode_access_token, get_user_id

logger = logging.getLogger(__name__)


# This is a test UAA public key
UAA_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA8oeihBQ1QVX3oPItRonk
ttUF7TyoTloZybRDL8lvZun7Z5xhxsLJmmKGF1sPO4eCnIZsvKPOilr6tjzQFFmC
QXAE3M/SMEI8/x2cO7UGFtf7tJQZ7LdkFL9GXHz5J1L2FtUTpwPhb37jYjxa3ZqL
1hOUjaVNPCWhuk11/MY99ziPPz0lyNHepYNILS6I17m5veoGFlNRJ3NoAb7WL0vI
yIT7HVi/L24UyzDTYL1XroBK/LXOTiWIYKoZHJCiGuiB2yMX8nvl7hWYojymey2D
mDVQ9nFMkDhUc8bZNpZXQlpsq41ZuI+tHBNuoHLFxWMDT3tY1QDgl4Z9vviKejxV
XwIDAQAB
-----END PUBLIC KEY-----"""

# An example UAA token
TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiI5NGNjN2Q3MjQ1N2Q0NWI0ODdmN" \
        "DE5NjYwMzNmMWU2ZiIsInN1YiI6IjY0ZDA5MmU2LTMwNDItNDk2OC1hMmUxLTI0Njg5YmJkOWVmMyIsInNjb3BlIjpbInNjaW0udXNlcmlkc" \
        "yIsInNjaW0ubWUiLCJwcm9maWxlIiwidXNlcl9hdHRyaWJ1dGVzIl0sImNsaWVudF9pZCI6InJhc19iYWNrc3RhZ2UiLCJjaWQiOiJyYXNfY" \
        "mFja3N0YWdlIiwiYXpwIjoicmFzX2JhY2tzdGFnZSIsImdyYW50X3R5cGUiOiJwYXNzd29yZCIsInVzZXJfaWQiOiI2NGQwOTJlNi0zMDQyL" \
        "TQ5NjgtYTJlMS0yNDY4OWJiZDllZjMiLCJvcmlnaW4iOiJ1YWEiLCJ1c2VyX25hbWUiOiJ1YWFfdXNlciIsImVtYWlsIjoidWFhLnVzZXJAZ" \
        "XhhbXBsZS5jb20iLCJhdXRoX3RpbWUiOjE1MTk3NDM4NzQsInJldl9zaWciOiIxNDU3MDEwMCIsImlhdCI6MTUxOTc0Mzg3NCwiZXhwIjoxN" \
        "TE5Nzg3MDc0LCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODAvdWFhL29hdXRoL3Rva2VuIiwiemlkIjoidWFhIiwiYXVkIjpbInNjaW0iL" \
        "CJyYXNfYmFja3N0YWdlIl19.SrD1H4aPPsO7m96044acm2X0g0eBOFaqTCORb26WH9o8d-wtxXprYb4I0QwrryEc1L7APm2PL0Ra7GhJOtNM" \
        "72ckqgaj3kr6vy5I_uBMvGgtnQolVhT7u7srcQGXkSqzUmku9nBwtmiSg0tTyOTn1NCh-HHvn6PZhmmxf1b3Uu0Q7mnd3HRUoL28ejgDn2Hl" \
        "91uU4dC-C4Dah0Pdk4dA7vMqmfjcuCMCUnFVVE3bNzZBhUGzC9KBPYu8q4SUx_WIxsJg1oTU99pz7391Bf2O0H3Z1PJTSyplf1hilQM6BbUL" \
        "PfH1KtVMgVp7nxARaj_UY0ILEZr-AZ0h6FywfQD2jw"

VALID_USER_ID = "64d092e6-3042-4968-a2e1-24689bbd9ef3"
VALID_USER_NAME = "uaa_user"


def get_pk():
    return UAA_PUBLIC_KEY


class TestTokenDecode(unittest.TestCase):

    def setUp(self):
        self.app = app
        app.config["UAA_PUBLIC_KEY"] = UAA_PUBLIC_KEY

    def test_valid_token(self, ):
        with app.app_context():
            decoded_token = decode_access_token(TOKEN, False)
            logger.error(decoded_token)
            self.assertEqual(VALID_USER_ID, decoded_token.get('user_id'))
            self.assertEqual(VALID_USER_NAME, decoded_token.get('user_name'))

    def test_get_user_name(self):
        with app.app_context():
            user_id = get_user_id(TOKEN, False)
            self.assertEqual(VALID_USER_ID, user_id)

    def test_raise_500_on_decode_error(self):
        with app.app_context():
            with self.assertRaises(InternalServerError):
                decode_access_token("invalid_token", False)



