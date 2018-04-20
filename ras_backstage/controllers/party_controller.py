import json
import logging

from structlog import wrap_logger

from ras_backstage import app
from ras_backstage.common.requests_handler import request_handler
from ras_backstage.exception.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_party_by_business_id(party_id, collection_exercise_id=None):
    logger.debug('Retrieving business party', party_id=party_id)
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/businesses/id/{party_id}'
    params = {"collection_exercise_id": collection_exercise_id, "verbose": True}
    response = request_handler('GET', url, params=params, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving business party', party_id=party_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved business party', party_id=party_id)
    return response.json()


def get_party_by_respondent_id(party_id):
    logger.debug('Retrieving respondent party', party_id=party_id)
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/respondents/id/{party_id}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving respondent party', party_id=party_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved respondent party', party_id=party_id)
    return response.json()


def get_party_by_ru_ref(ru_ref):
    logger.debug('Retrieving reporting unit', ru_ref=ru_ref)
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/parties/type/B/ref/{ru_ref}'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error retrieving reporting unit', ru_ref=ru_ref)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved reporting unit', ru_ref=ru_ref)
    return response.json()


def get_businesses_by_search(query):
    logger.debug('Retrieving businesses by search query', query=query)
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/businesses/search'
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'], params={"query": query})

    if response.status_code != 200:
        logger.error('Error retrieving businesses by search query', query=query)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved businesses by search query')
    return json.loads(response.text)


def update_respondent_details(respondent_id, respondent_contact_details):
    logger.debug('Updating respondent details', respondent_id=respondent_id)
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/respondents/id/{respondent_id}'
    payload = {
        "firstName": respondent_contact_details['first_name'],
        "lastName": respondent_contact_details['last_name'],
        "telephone": respondent_contact_details['telephone'],
        "email_address": respondent_contact_details['email_address'],
        "new_email_address": respondent_contact_details['new_email_address']
        }

    response = request_handler('PUT', url, json=payload, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Error updating respondent details', respondent_id=respondent_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully updated respondent details')


def resend_verification_email(party_id):
    logger.debug('Resending verification email', party_id=party_id)
    url = app.config['RAS_PARTY_RESEND_VERIFICATION_EMAIL'].format(party_id)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Failed to resend verification email', party_id=party_id)
        raise ApiError(url=url, status_code=response.status_code)

    logger.debug('Successfully resent verification email')


def put_respondent_account_status(change_data):
    logger.debug('Changing respondent account status', party_id=change_data['party_id'], account_status=change_data['status_change'])
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/respondents/edit-account-status'
    response = request_handler('PUT', url, auth=app.config['BASIC_AUTH'], json=change_data)

    if response.status_code != 200:
        logger.error('Error updating respondent account status', party_id=change_data['party_id'])
        raise ApiError(url, response.status_code)

    logger.debug('Successfully changed respondent account status', party_id=change_data['party_id'], account_status=change_data['status_change'])


def get_respondent_by_email(email):
    logger.debug('Getting respondent by email')
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/respondents/email'

    response = request_handler('GET', url, json=email, auth=app.config['BASIC_AUTH'])

    if response.status_code == 404:
        logger.debug("No respondent found", status_code=response.status_code)
        return {"Response": "No respondent found"}
    elif response.status_code != 200:
        logger.error('Error retrieving respondent')
        raise ApiError(url, response.status_code)
    logger.debug("Successfully retrieved respondent")
    return response.json()


def put_respondent_enrolment_status(enrolment):
    logger.debug('Changing enrolment status', enrolment=enrolment)
    url = f'{app.config["RAS_PARTY_SERVICE"]}party-api/v1/respondents/change_enrolment_status'
    response = request_handler('PUT', url, auth=app.config['BASIC_AUTH'], json=enrolment)

    if response.status_code != 200:
        logger.error('Failed to change enrolment status', enrolment=enrolment)
        raise ApiError(url=url, status_code=response.status_code)

    logger.debug('Successfully changed enrolment status')
