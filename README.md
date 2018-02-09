# ras-backstage
[![Build Status](https://travis-ci.org/ONSdigital/ras-backstage.svg?branch=master)](https://travis-ci.org/ONSdigital/ras-backstage)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/38f97350260a4819aa64c4a4d19f6d1d)](https://www.codacy.com/app/ONS/ras-backstage?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ONSdigital/ras-backstage&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/ONSdigital/ras-backstage/branch/master/graph/badge.svg)](https://codecov.io/gh/ONSdigital/ras-backstage)

## Description
API to handle interfacing between the Ras-Backstage and internal micro-services

## Setup
Created using python 3.6

Install dependencies using [pipenv](https://docs.pipenv.org/index.html)
```
pip install -U pipenv
pipenv install
```

or using make
```
make build
```

Start server
```
pipenv run python run.py
```

or with docker

```bash
docker build . -t ras-backstage
docker run -p 8080:8080 ras-backstage
```

or with make
```
make start
```


## Run Tests
Install test dependencies using pipenv
```
pipenv install --dev
```

Run tests with coverage
```
pipenv run python run_tests.py
```

Run flake8 check
```
pipenv check --style .
```

Run tests with make
```
make test
```

## Swagger
A swagger UI definition of the API is automatically generated using Flask-RESTPlus and can be found at the root of the application, by default [localhost:8001]('http://localhost:8001')

## Configuration
The application is configured with environment variables, these can be found in [config.py](config.py)

Environment variables available for configuration are listed below:

| Environment Variable            | Description                                        | Default
|---------------------------------|----------------------------------------------------|-------------------------------
| NAME                            | Name of application                                | 'ras-backstage'
| VERSION                         | Version number of application                      | '0.0.1' (manually update as application updates)
| LOGGING_LEVEL                   | Filter log output by minimum logging level         | 'INFO'
| APP_SETTINGS                    | Which config object to use                         | 'Config' (use DevelopmentConfig) for development
| SECRET_KEY                      | Secret key used by flask                           | 'ONS_DUMMY_KEY'
| SECURITY_USER_NAME              | Username for basic auth                            | 'admin'
| SECURITY_USER_PASSWORD          | Password for basic auth                            | 'secret'
| JWT_ALGORITHM                   | Algotithm used to code JWT                         | 'HS256'
| JWT_SECRET                      | SECRET used to code JWT                            | None
| DJANGO_CLIENT_ID                | Client ID for OAuth service                        | None
| DJANGO_CLIENT_SECRET            | Client secret for OAuth service                    | None
| USE_UAA                         | Switches UAA authentication                        | 1


For each external application which frontstage communicates with there are 3 environment variables e.g. for the RM case service:

| Environment Variable                           | Description                                      | Default
|------------------------------------------------|--------------------------------------------------|-------------------------------
| RM_COLLECTION_EXERCISE_SERVICE_PROTOCOL        | Protocol used for RM collection exercise service | 'http'
| RM_COLLECTION_EXERCISE_SERVICE_HOST            | Host address for RM collection exercise service  | 'localhost'
| RM_COLLECTION_EXERCISE_SERVICE_PORT            | Port for RM collection exercise service          | '8145'

The services these variables exist for are listed below with the beginnings of their variables and their github links:

| Service                         | Start of variables          | Github
|---------------------------------|-----------------------------|-----------------------------
| Collection exercise service     | RM_COLLECTION_EXERCISE      | https://github.com/ONSdigital/rm-collection-exercise-service
| Collection instrument service   | RAS_COLLECTION_INSTRUMENT   | https://github.com/ONSdigital/ras-collection-instrument
| Survey service                  | RM_SURVEY_SERVICE           | https://github.com/ONSdigital/rm-survey-service
| Sample service                  | RM_SAMPLE_SERVICE           | https://github.com/ONSdigital/rm-sample-service
| Party service                   | RAS_PARTY_SERVICE           | https://github.com/ONSdigital/ras-party
| Secure message service          | RAS_SECURE_MESSAGE_SERVICE  | https://github.com/ONSdigital/ras-secure-message
| Oauth service                   | RAS_OAUTH_SERVICE           | https://github.com/ONSdigital/django-oauth2-test
