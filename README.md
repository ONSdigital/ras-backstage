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

Start server
```
pipenv run python run.py
```

or with docker

```bash
docker build . -t ras-backstage
docker run -p 8080:8080 ras-backstage
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

## Swagger
A swagger UI definition of the API is automatically generated using Flask-RESTPlus and can be found at the root of the application, by default [localhost:8001]('http://localhost:8001')

## Configuration
The application is configured with environment variables, these can be found in [config.py](config.py)
