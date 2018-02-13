import os


class Config(object):
    DEBUG = os.getenv('DEBUG', False)
    TESTING = False
    VERSION = os.getenv('VERSION', '0.0.3')
    PORT = os.getenv('PORT', 8001)
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')
    SECURITY_USER_NAME = os.getenv('SECURITY_USER_NAME')
    SECURITY_USER_PASSWORD = os.getenv('SECURITY_USER_PASSWORD')
    BASIC_AUTH = (SECURITY_USER_NAME, SECURITY_USER_PASSWORD)
    DJANGO_CLIENT_ID = os.getenv('DJANGO_CLIENT_ID')
    DJANGO_CLIENT_SECRET = os.getenv('DJANGO_CLIENT_SECRET')
    DJANGO_BASIC_AUTH = (DJANGO_CLIENT_ID, DJANGO_CLIENT_SECRET)
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_SECRET = os.getenv('JWT_SECRET')

    # TODO: remove once UAA is implemented and use user supplied username/password
    USERNAME = os.getenv('RAS_BACKSTAGE_USERNAME', 'user')
    PASSWORD = os.getenv('RAS_BACKSTAGE_PASSWORD', 'pass')

    RAS_OAUTH_SERVICE_HOST = os.getenv('RAS_OAUTH_SERVICE_HOST', 'localhost')
    RAS_OAUTH_SERVICE_PORT = os.getenv('RAS_OAUTH_SERVICE_PORT', 8040)
    RAS_OAUTH_SERVICE_PROTOCOL = os.getenv('RAS_OAUTH_SERVICE_PROTOCOL', 'http')
    RAS_OAUTH_SERVICE = '{}://{}:{}/'.format(RAS_OAUTH_SERVICE_PROTOCOL,
                                             RAS_OAUTH_SERVICE_HOST,
                                             RAS_OAUTH_SERVICE_PORT)

    RAS_SECURE_MESSAGING_SERVICE_HOST = os.getenv('RAS_SECURE_MESSAGING_SERVICE_HOST', 'localhost')
    RAS_SECURE_MESSAGING_SERVICE_PORT = os.getenv('RAS_SECURE_MESSAGING_SERVICE_PORT', 5050)
    RAS_SECURE_MESSAGING_SERVICE_PROTOCOL = os.getenv('RAS_SECURE_MESSAGING_SERVICE_PROTOCOL',
                                                      'http')
    RAS_SECURE_MESSAGING_SERVICE = '{}://{}:{}/'.format(RAS_SECURE_MESSAGING_SERVICE_PROTOCOL,
                                                        RAS_SECURE_MESSAGING_SERVICE_HOST,
                                                        RAS_SECURE_MESSAGING_SERVICE_PORT)

    RM_CASE_SERVICE_HOST = os.getenv('RM_CASE_SERVICE_HOST', 'localhost')
    RM_CASE_SERVICE_PORT = os.getenv('RM_CASE_SERVICE_PORT', 8171)
    RM_CASE_SERVICE_PROTOCOL = os.getenv('RM_CASE_SERVICE_PROTOCOL', 'http')
    RM_CASE_SERVICE = '{}://{}:{}/'.format(RM_CASE_SERVICE_PROTOCOL,
                                           RM_CASE_SERVICE_HOST,
                                           RM_CASE_SERVICE_PORT)

    RM_COLLECTION_EXERCISE_SERVICE_HOST = os.getenv('RM_COLLECTION_EXERCISE_SERVICE_HOST',
                                                    'localhost')
    RM_COLLECTION_EXERCISE_SERVICE_PORT = os.getenv('RM_COLLECTION_EXERCISE_SERVICE_PORT',
                                                    8145)
    RM_COLLECTION_EXERCISE_SERVICE_PROTOCOL = os.getenv('RM_COLLECTION_EXERCISE_SERVICE_PROTOCOL',
                                                        'http')
    RM_COLLECTION_EXERCISE_SERVICE = '{}://{}:{}/'.format(RM_COLLECTION_EXERCISE_SERVICE_PROTOCOL,
                                                          RM_COLLECTION_EXERCISE_SERVICE_HOST,
                                                          RM_COLLECTION_EXERCISE_SERVICE_PORT)

    RAS_COLLECTION_INSTRUMENT_SERVICE_HOST = os.getenv('RAS_COLLECTION_INSTRUMENT_SERVICE_HOST',
                                                       'localhost')
    RAS_COLLECTION_INSTRUMENT_SERVICE_PORT = os.getenv('RAS_COLLECTION_INSTRUMENT_SERVICE_PORT',
                                                       8002)
    RAS_COLLECTION_INSTRUMENT_SERVICE_PROTOCOL = os.getenv('RAS_COLLECTION_INSTRUMENT_SERVICE_PROTOCOL',
                                                           'http')
    RAS_COLLECTION_INSTRUMENT_SERVICE = '{}://{}:{}/'.format(RAS_COLLECTION_INSTRUMENT_SERVICE_PROTOCOL,
                                                             RAS_COLLECTION_INSTRUMENT_SERVICE_HOST,
                                                             RAS_COLLECTION_INSTRUMENT_SERVICE_PORT)

    RAS_PARTY_SERVICE_HOST = os.getenv('RAS_PARTY_SERVICE_HOST', 'localhost')
    RAS_PARTY_SERVICE_PORT = os.getenv('RAS_PARTY_SERVICE_PORT', 8081)
    RAS_PARTY_SERVICE_PROTOCOL = os.getenv('RAS_PARTY_SERVICE_PROTOCOL', 'http')
    RAS_PARTY_SERVICE = '{}://{}:{}/'.format(RAS_PARTY_SERVICE_PROTOCOL,
                                             RAS_PARTY_SERVICE_HOST,
                                             RAS_PARTY_SERVICE_PORT)

    RM_SURVEY_SERVICE_HOST = os.getenv('RM_SURVEY_SERVICE_HOST', 'localhost')
    RM_SURVEY_SERVICE_PORT = os.getenv('RM_SURVEY_SERVICE_PORT', 8080)
    RM_SURVEY_SERVICE_PROTOCOL = os.getenv('RM_SURVEY_SERVICE_PROTOCOL', 'http')
    RM_SURVEY_SERVICE = '{}://{}:{}/'.format(RM_SURVEY_SERVICE_PROTOCOL,
                                             RM_SURVEY_SERVICE_HOST,
                                             RM_SURVEY_SERVICE_PORT)

    RM_SAMPLE_SERVICE_HOST = os.getenv('RM_SAMPLE_SERVICE_HOST', 'localhost')
    RM_SAMPLE_SERVICE_PORT = os.getenv('RM_SAMPLE_SERVICE_PORT', 8125)
    RM_SAMPLE_SERVICE_PROTOCOL = os.getenv('RM_SAMPLE_SERVICE_PROTOCOL', 'http')
    RM_SAMPLE_SERVICE = '{}://{}:{}/'.format(RM_SAMPLE_SERVICE_PROTOCOL,
                                             RM_SAMPLE_SERVICE_HOST,
                                             RM_SAMPLE_SERVICE_PORT)


class DevelopmentConfig(Config):
    DEBUG = os.getenv('DEBUG', True)
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')
    SECURITY_USER_NAME = os.getenv('SECURITY_USER_NAME', 'admin')
    SECURITY_USER_PASSWORD = os.getenv('SECURITY_USER_PASSWORD', 'secret')
    BASIC_AUTH = (SECURITY_USER_NAME, SECURITY_USER_PASSWORD)
    DJANGO_CLIENT_ID = os.getenv('DJANGO_CLIENT_ID', 'ons@ons.gov')
    DJANGO_CLIENT_SECRET = os.getenv('DJANGO_CLIENT_SECRET', 'password')
    DJANGO_BASIC_AUTH = (DJANGO_CLIENT_ID, DJANGO_CLIENT_SECRET)
    JWT_SECRET = os.getenv('JWT_SECRET', 'testsecret')


class TestingConfig(DevelopmentConfig):
    DEBUG = True
    Testing = True
