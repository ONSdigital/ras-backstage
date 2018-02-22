from flask import current_app
import jwt


def decode_access_token(access_token):
    decoded_jwt = jwt.decode(
        access_token,
        verify=True,
        algorithms=None,
        key=current_app.config['UAA_PUBLIC_KEY'],
        audience='ras_backstage',
        leeway=10,
    )
    return decoded_jwt


def get_user_id(access_token):
    decoded_jwt = decode_access_token(access_token)
    return decoded_jwt.get('user_id')

