import logging

from flask import abort
import jwt

from ras_backstage.authentication.uaa import get_uaa_public_key


logger = logging.getLogger(__name__)


def decode_access_token(access_token, verify=True):

    try:
        decoded_jwt = jwt.decode(
            access_token,
            verify=verify,
            algorithms=None,
            key=get_uaa_public_key(),
            audience='ras_backstage',
            leeway=10,
        )
        return decoded_jwt
    except jwt.DecodeError:
        logger.error(f"Unable to decode token {access_token} - confirm the UAA public key is correct")
        abort(500)


def get_user_id(access_token, verify=True):
    decoded_jwt = decode_access_token(access_token, verify)
    user_id = decoded_jwt.get("user_id")
    logger.debug(f"Retrieved user_id from access token {user_id}")
    return user_id
