import json
import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_messages_list(encoded_jwt, message_args):
    logger.debug('Retrieving messages list', label=message_args.get('label'))
    url = '{}{}'.format(app.config['RAS_SECURE_MESSAGING_SERVICE'], 'messages')
    headers = {"Authorization": encoded_jwt}
    response = request_handler('GET', url, headers=headers, params=message_args)

    if response.status_code != 200:
        logger.error('Error retrieving the messages list', label=message_args.get('label'))
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved the messages list', label=message_args.get('label'))
    return json.loads(response.text)


def get_message(encoded_jwt, message_id, is_draft):
    logger.debug('Retrieving message', message_id=message_id, is_draft=is_draft)
    endpoint = 'draft/' if is_draft == 'true' else 'message/'
    url = '{}{}{}'.format(app.config['RAS_SECURE_MESSAGING_SERVICE'], endpoint, message_id)
    headers = {"Authorization": encoded_jwt}
    response = request_handler('GET', url, headers=headers)

    if response.status_code != 200:
        logger.error('Error retrieving the messages', message_id=message_id, is_draft=is_draft)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved message', message_id=message_id, is_draft=is_draft)
    return json.loads(response.text)


def update_label(encoded_jwt, message_id, label, action):
    logger.debug('Updating label', message_id=message_id, label=label, action=action)
    url = '{}{}'.format(app.config['RAS_SECURE_MESSAGING_SERVICE'],
                        'message/{}/modify'.format(message_id))
    headers = {"Authorization": encoded_jwt}
    data = {"label": label, "action": action}
    response = request_handler('PUT', url, headers=headers, json=data)

    if not response or response.status_code != 200:
        logger.error('Error updating label', message_id=message_id, label=label, action=action)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully updated label', message_id=message_id, label=label, action=action)


def send_message(encoded_jwt, message_json):
    logger.debug('Sending message')
    headers = {"Authorization": encoded_jwt}
    url = '{}{}'.format(app.config['RAS_SECURE_MESSAGING_SERVICE'], 'message/send')
    response = request_handler('POST', url, headers=headers, json=message_json)

    if response.status_code != 201:
        logger.error('Failed to send message')
        raise ApiError(url, response.status_code)

    message = json.loads(response.text)
    logger.debug('Message sent successfully', message_id=message['msg_id'])
    return message


def save_draft(encoded_jwt, message_json):
    logger.debug('Saving draft')
    headers = {"Authorization": encoded_jwt}

    url = '{}{}'.format(app.config['RAS_SECURE_MESSAGING_SERVICE'], 'draft/save')
    response = request_handler('POST', url, headers=headers, json=message_json)

    if response.status_code != 201:
        logger.error('Failed to save draft')
        raise ApiError(url, response.status_code)

    message = json.loads(response.text)
    logger.debug('Draft saved successfully', message_id=message['msg_id'])
    return message


def update_draft(encoded_jwt, message_json):
    logger.debug('Updating draft', message_id=message_json['msg_id'])
    headers = {"Authorization": encoded_jwt}

    url = '{}{}'.format(app.config['RAS_SECURE_MESSAGING_SERVICE'],
                        'draft/{}/modify'.format(message_json['msg_id']))
    response = request_handler('PUT', url, headers=headers, json=message_json)

    if response.status_code != 200:
        logger.error('Failed to update draft', message_id=message_json['msg_id'])
        raise ApiError(url, response.status_code)

    message = json.loads(response.text)
    logger.debug('Draft updated successfully', message_id=message['msg_id'])
    return message
