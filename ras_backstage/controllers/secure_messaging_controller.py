import json
import logging
from json import JSONDecodeError

import jwt
from flask import current_app
from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.authentication import token_decoder
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError

logger = wrap_logger(logging.getLogger(__name__))


def get_messages_list(encoded_jwt, message_args):
    logger.debug('Retrieving messages list', label=message_args.get('label'))
    url = f"{app.config['RAS_SECURE_MESSAGING_SERVICE']}v2/messages"
    headers = _create_authorization_header(encoded_jwt)

    response = request_handler('GET', url, headers=headers, params=message_args)

    if response.status_code != 200:
        logger.error('Error retrieving the messages list', label=message_args.get('label'))
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved the messages list', label=message_args.get('label'))
    return json.loads(response.text)


def get_message(encoded_jwt, message_id, is_draft):
    logger.debug('Retrieving message', message_id=message_id, is_draft=is_draft)
    endpoint = 'draft/' if is_draft == 'true' else 'message/'
    url = f"{app.config['RAS_SECURE_MESSAGING_SERVICE']}{endpoint}{message_id}"
    headers = _create_authorization_header(encoded_jwt)
    response = request_handler('GET', url, headers=headers)

    if response.status_code != 200:
        logger.error('Error retrieving the messages', message_id=message_id, is_draft=is_draft)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved message', message_id=message_id, is_draft=is_draft)
    return json.loads(response.text)


def get_threads_list(encoded_jwt, message_args):
    logger.debug('Retrieving threads list')
    url = f"{app.config['RAS_SECURE_MESSAGING_SERVICE']}threads"
    headers = _create_authorization_header(encoded_jwt)

    response = request_handler('GET', url, headers=headers, params=message_args)

    if response.status_code != 200:
        logger.error('Error retrieving the threads list')
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved the threads list')

    try:
        return response.json()
    except ValueError:
        logger.error('Failed to decode response json from get threads')
        raise ApiError(url=url)


def get_thread_by_id(encoded_jwt, thread_id):
    """
    The method return all the message part of a thread.
    :param encoded_jwt:  is the security token.
    :param thread_id: is the id of the thread selected.
    :return: a list of messages sent/received part of conversation thread
    """
    url = f"{app.config['RAS_SECURE_MESSAGING_SERVICE']}v2/threads/{thread_id}"

    headers = _create_authorization_header(encoded_jwt)
    response = request_handler('GET', url, headers=headers)

    if response.status_code != 200:
        logger.error('Error retrieving the messages', thread_id=thread_id)
        raise ApiError(url, response.status_code)

    try:
        return response.json()
    except (JSONDecodeError, ValueError):
        logger.exception("Error decoding JSON response")
        raise JSONDecodeError


def update_label(encoded_jwt, message_id, label, action):
    logger.debug('Updating label', message_id=message_id, label=label, action=action)
    url = f"{app.config['RAS_SECURE_MESSAGING_SERVICE']}v2/messages/modify/{message_id}"
    headers = _create_authorization_header(encoded_jwt)
    data = {"label": label, "action": action}
    response = request_handler('PUT', url, headers=headers, json=data)

    if not response or response.status_code != 200:
        logger.error('Error updating label', message_id=message_id, label=label, action=action)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully updated label', message_id=message_id, label=label, action=action)


def send_message(encoded_jwt, message_json):
    logger.debug('Sending message')
    headers = _create_authorization_header(encoded_jwt)
    url = f"{app.config['RAS_SECURE_MESSAGING_SERVICE']}v2/messages"
    response = request_handler('POST', url, headers=headers, json=message_json)

    if response.status_code != 201:
        logger.error('Failed to send message')
        raise ApiError(url, response.status_code)

    message = json.loads(response.text)
    logger.debug('Message sent successfully', message_id=message['msg_id'])
    return message


def save_draft(encoded_jwt, message_json):
    logger.debug('Saving draft')
    headers = _create_authorization_header(encoded_jwt)

    url = f"{app.config['RAS_SECURE_MESSAGING_SERVICE']}draft/save"
    response = request_handler('POST', url, headers=headers, json=message_json)

    if response.status_code != 201:
        logger.error('Failed to save draft')
        raise ApiError(url, response.status_code)

    message = json.loads(response.text)
    logger.debug('Draft saved successfully', message_id=message['msg_id'])
    return message


def update_draft(encoded_jwt, message_json):
    logger.debug('Updating draft', message_id=message_json['msg_id'])
    headers = _create_authorization_header(encoded_jwt)

    url = f"{app.config['RAS_SECURE_MESSAGING_SERVICE']}draft/{message_json['msg_id']}/modify"
    response = request_handler('PUT', url, headers=headers, json=message_json)

    if response.status_code != 200:
        logger.error('Failed to update draft', message_id=message_json['msg_id'])
        raise ApiError(url, response.status_code)

    message = json.loads(response.text)
    logger.debug('Draft updated successfully', message_id=message['msg_id'])
    return message


def _create_authorization_header(access_token):
    if current_app.config.get('USE_UAA'):
        logger.info(f'Received token {access_token}')
        token = token_decoder.decode_access_token(access_token)
        user_id = token.get('user_id')
    else:
        user_id = "BRES"
    secret = app.config['RAS_SECURE_MESSAGING_JWT_SECRET']
    sm_token = jwt.encode({'party_id': user_id, 'role': 'internal'}, secret, algorithm='HS256')
    return {"Authorization": sm_token}
