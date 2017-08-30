test_config = """
service:
    NAME: ras-backstage
    VERSION: 0.0.1
    SCHEME: http
    HOST: 0.0.0.0
    PORT: 8000
    LOG_LEVEL: error
    SECRET_KEY: secret
    SECURITY_USER_NAME: dummy_user
    SECURITY_USER_PASSWORD: dummy_password

dependencies:
    oauth2-service:
        scheme: http
        host: mockhost
        port: 4444
        authorization_endpoint: "/web/authorize/"
        token_endpoint: "/api/v1/tokens/"
        admin_endpoint: "/api/account/create"
        activate_endpoint: "/api/account/activate"
        client_id: "ons@ons.gov"
        client_secret: "password"


"""
