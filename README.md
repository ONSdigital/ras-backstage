# ras-backstage
[![Build Status](https://travis-ci.org/ONSdigital/ras-backstage.svg?branch=master)](https://travis-ci.org/ONSdigital/ras-backstage)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/38f97350260a4819aa64c4a4d19f6d1d)](https://www.codacy.com/app/ONS/ras-backstage?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ONSdigital/ras-backstage&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/ONSdigital/ras-backstage/branch/master/graph/badge.svg)](https://codecov.io/gh/ONSdigital/ras-backstage)

## Description

This service acts as a reverse proxy to RAS services, with added JWT protection to ensure a client/user is authenticated to the RAS OAuth server. The primary client of ras-backstage is expected to be ras-backstage-ui.

The services which can be proxied to are those listed in the 'dependencies' section of the config.yaml file, specifically:

- case-service
- collection-exercise-service
- collection-instrument-service
- survey-service
- secure-message-service
- party-service

URLs into this service are routed to the relevant downstream service by inspecting the first part of the 'path' of the URL (see: https://en.wikipedia.org/wiki/URL ). For example, given the URL `http://localhost:8080/case-service/.../`,
the 'case-service' part of the URL corresponds to the related configuration file entry. The remainder of the URL is passed through to the downstream service. Thus the routing is performed
statically based on the service configuration. Note that service configuration is overridden in each deployed environment via environmental variables to configure the scheme, host and port of the
target downstream service. E.g. if the following environment variables are configured as:

```
export case-service.scheme=http
export case-service.host=0.0.0.0
export case-service.port=5000
```

Then the example URL `http://localhost:8080/case-service/.../` will be proxied to `http://0.0.0.0:5000/...`.

All attempts to proxy through ras-backstage in this way will encounter JWT protection, and will need to supply a valid JWT token within the `Authorization` request header. A valid token is obtained via the `sign_in` endpoint,
which accepts username and password as JSON body parameters. If the supplied credentials are found on the OAuth2 server using the OAuth 'Resource owner password credentials' flow ( https://tools.ietf.org/html/rfc6749#section-4.3), then sign_in is successful and an encoded JWT is returned
The JWT may subsequently be used to proxy through to RAS services.


Run the application
-------------------
Install dependencies for the application using pip
```
pip install -r requirements.txt
```
Once these have been installed the app can be run from the ras-backstage directory using the following
```
$ python run.py
```

Test the application
--------------------
Install dependencies for the tests using pip
```
pip install -r test-requirements.txt
```

Once these have been installed the tests can be run from the ras-backstage directory using the following
```
$ pytest
```

Test the response
-----------------

Now open up a prompt to test out your API using curl
```
$ curl http://127.0.0.1:5050/info
{
  "name": "ras-backstage",
  "version": "0.0.1"
}
```
## Configuration

Environment variables available for configuration are listed below:

| Environment Variable            | Description                                        | Default
|---------------------------------|----------------------------------------------------|-------------------------------
| NAME                            | Name of application                                | 'ras-backstage'
| LOGGING_LEVEL                   | Used to set application logging level              | 'INFO'