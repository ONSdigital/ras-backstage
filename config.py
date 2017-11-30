import os


class Config(object):
    DEBUG = os.getenv('DEBUG', False)
    TESTING = False
    NAME = 'ras-backstage'
    VERSION = os.getenv('VERSION', '0.0.1')
    PORT = os.getenv('PORT', 8083)
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')
    SECURITY_USER_NAME = os.getenv('SECURITY_USER_NAME')
    SECURITY_USER_PASSWORD = os.getenv('SECURITY_USER_PASSWORD')
    BASIC_AUTH = (SECURITY_USER_NAME, SECURITY_USER_PASSWORD)
    DJANGO_CLIENT_ID = os.getenv('DJANGO_CLIENT_ID')
    DJANGO_CLIENT_SECRET = os.getenv('DJANGO_CLIENT_SECRET')
    DJANGO_BASIC_AUTH = (DJANGO_CLIENT_ID, DJANGO_CLIENT_SECRET)
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_SECRET = os.getenv('JWT_SECRET')

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


class DevelopmentConfig(Config):
    DEBUG = os.getenv('DEBUG', True)
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')
    SECURITY_USER_NAME = os.getenv('SECURITY_USER_NAME', 'test_user')
    SECURITY_USER_PASSWORD = os.getenv('SECURITY_USER_PASSWORD', 'test_password')
    BASIC_AUTH = (SECURITY_USER_NAME, SECURITY_USER_PASSWORD)
    DJANGO_CLIENT_ID = os.getenv('DJANGO_CLIENT_ID', 'test@test.test')
    DJANGO_CLIENT_SECRET = os.getenv('DJANGO_CLIENT_SECRET', 'testtest')
    DJANGO_BASIC_AUTH = (DJANGO_CLIENT_ID, DJANGO_CLIENT_SECRET)
    JWT_SECRET = os.getenv('JWT_SECRET', 'vrwgLNWEffe45thh545yuby')


class TestingConfig(DevelopmentConfig):
    DEBUG = True
    Testing = True
