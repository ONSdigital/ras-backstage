import logging

from flask import abort
import jwt
from jwt import DecodeError

from ras_backstage.authentication.uaa import get_uaa_public_key


logger = logging.getLogger(__name__)


def decode_access_token(access_token):

    try:
        decoded_jwt = jwt.decode(
            access_token,
            verify=True,
            algorithms=None,
            key=get_uaa_public_key(),
            audience='ras_backstage',
            leeway=10,
        )
        return decoded_jwt
    except DecodeError:
        logger.error(f"Unable to decode token {access_token} - confirm the UAA public key is correct")
        abort(500)


def get_user_id(access_token):
    decoded_jwt = decode_access_token(access_token)
    if decoded_jwt:
        return decoded_jwt.get('user_id')
