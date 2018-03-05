import jwt

from ras_backstage.authentication.uaa import get_uaa_public_key


def decode_access_token(access_token):
    uaa_public_key = get_uaa_public_key()
    decoded_jwt = jwt.decode(
        access_token,
        key=uaa_public_key,
        audience='ras_backstage',
        leeway=10,
    )
    return decoded_jwt
