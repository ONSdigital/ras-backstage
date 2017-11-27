import json
import logging

import requests
from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_messages_list(encoded_jwt, label="", limit=1000):
    logger.debug('Attempting to retrieve the messages list', label=label)
    url = '{}{}'.format(app.config['SECURE_MESSAGING_SERVICE'], 'messages')
    headers = {"Authorization": encoded_jwt}
    response = requests.get(url, headers=headers, params={"label": label, "limit": limit})

    if response.status_code != 200:
        logger.error('Error retrieving the messages list', label=label, status_code=response.status_code)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved the messages list', label=label)
    return json.loads(response.text)


def get_message(encoded_jwt, message_id, is_draft):
    logger.debug('Attempting to retrieve message', message_id=message_id, is_draft=is_draft)
    endpoint = 'draft/' if is_draft == 'true' else 'message/'
    url = '{}{}{}'.format(app.config['SECURE_MESSAGING_SERVICE'], endpoint, message_id)
    headers = {"Authorization": encoded_jwt}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        logger.error('Error retrieving the messages', status_code=response.status_code, message_id=message_id, is_draft=is_draft)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved message', message_id=message_id, is_draft=is_draft)
    return json.loads(response.text)


def remove_unread_label(encoded_jwt, message_id):
    logger.debug('Attempting to remove unread label', message_id=message_id)
    url = '{}{}'.format(app.config['SECURE_MESSAGING_SERVICE'], 'message/{}/modify'.format(message_id))
    headers = {"Authorization": encoded_jwt}
    data = {"label": 'UNREAD', "action": 'remove'}
    response = requests.put(url, headers=headers, json=data)

    if not response or response.status_code != 200:
        logger.error('Error removing unread message label', status_code=response.status_code, message_id=message_id)
        unread_label_removed = False
    else:
        logger.debug('Successfully removed unread label')
        unread_label_removed = True

    return {"unread_label_removed": unread_label_removed}

