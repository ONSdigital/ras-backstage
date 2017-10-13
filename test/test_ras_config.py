import unittest
from unittest.mock import patch

import yaml

from ras_backstage.ras_config import ras_config
from ras_backstage.ras_config.ras_config import RasConfig, RasDependencyError

CONFIG_FRAGMENT = """
service:
    name: my-service
    version: 1.0.0

dependencies:
    ras-postgres:
        host: my-host
        uri: my-database-uri
        schema: my-schema
    ras-rabbit:
        hostname: 127.0.0.1
        password: blah
        protocols:
            amqp:
                host: 0.0.0.0
            other:
                host: 1.2.3.4

features:
    config-true-flag: 'true'
    config-false-flag: 'false'
    config-bool-true: true
"""

CONFIG_NO_DEPENDENCIES = """
INFO:
    NAME: my-service
    VERSION: 1.0.0
"""

VCAP_SERVICES_FRAGMENT = """
{
  "rds": [
   {
    "credentials": {
     "db_name": "dbytrzj0avkc2o0oz",
     "host": "mvp-applicationdb.cef6vnd8djsq.eu-central-1.rds.amazonaws.com",
     "password": "x1skp4kj1or5y961yyjdb4lzt",
     "uri": "postgres://overridden",
     "username": "ub558d0i1xybbmbd"
    },
    "label": "rds",
    "name": "ras-postgres",
    "plan": "shared-psql",
    "provider": null,
    "syslog_drain_url": null,
    "tags": [
     "database",
     "RDS",
     "postgresql"
    ],
    "volume_mounts": []
   }
  ]
 }
"""


VCAP_APP_FRAGMENT = """
 {
  "application_id": "85fb7b49-f346-4c55-a1f7-f9f4d657da8c",
  "application_name": "ras-party-service-test",
  "application_uris": [
   "ras-party-service-test.apps.mvp.onsclofo.uk"
  ],
  "application_version": "82d14db9-e90e-4acd-a91a-d17825044947",
  "cf_api": "https://api.system.mvp.onsclofo.uk",
  "limits": {
   "disk": 1024,
   "fds": 16384,
   "mem": 512
  },
  "name": "ras-party-service-test",
  "space_id": "28c531d3-a581-4a24-b45d-e6875b4e12f0",
  "space_name": "test",
  "uris": [
   "ras-party-service-test.apps.mvp.onsclofo.uk"
  ],
  "users": null,
  "version": "82d14db9-e90e-4acd-a91a-d17825044947"
 }
"""


class MockGetenv:

    def __call__(self, k, default=None):
        if k == 'VCAP_APPLICATION':
            return VCAP_APP_FRAGMENT
        elif k == 'VCAP_SERVICES':
            return VCAP_SERVICES_FRAGMENT


class TestRasConfig(unittest.TestCase):

    def test_config_enables_lookup_of_service_info(self):
        data = yaml.safe_load(CONFIG_FRAGMENT)
        c = RasConfig(data)

        service = c.service
        self.assertEqual(service['name'], "my-service")

    def test_get_dependency_returns_corresponding_config_section(self):
        c = RasConfig(yaml.safe_load(CONFIG_FRAGMENT))
        ras_postgres = c.dependency('ras-postgres')
        self.assertEqual(ras_postgres['uri'], 'my-database-uri')

    def test_get_nonexistent_dependency_raises_exception(self):
        c = RasConfig(yaml.safe_load(CONFIG_FRAGMENT))
        with self.assertRaises(RasDependencyError):
            c.dependency('ras-other')

    def test_get_dependency_returns_arbitrary_structure(self):
        c = RasConfig(yaml.safe_load(CONFIG_FRAGMENT))
        ras_rabbit = c.dependency('ras-rabbit')
        self.assertEqual(ras_rabbit['protocols'], {'amqp': {'host': '0.0.0.0'}, 'other': {'host': '1.2.3.4'}})

    @patch('ras_backstage.ras_config.ras_config.getenv', new_callable=MockGetenv)
    def test_config_overrides_values_from_cloudfoundry(self, _):
        c = ras_config.make(yaml.safe_load(CONFIG_FRAGMENT))
        ras_postgres = c.dependency('ras-postgres')
        self.assertEqual(ras_postgres['uri'], 'postgres://overridden')

        # Also test the dependencies accessor
        postgres_found = False
        for d in c.dependencies():
            if d[0] == 'ras-postgres':
                self.assertEqual(d[1]['uri'], 'postgres://overridden')
                postgres_found = True

        self.assertTrue(postgres_found)

    @patch('ras_backstage.ras_config.ras_config.getenv', new_callable=MockGetenv)
    def test_config_only_overrides_when_key_present_in_cloudfoundry(self, _):
        c = ras_config.make(yaml.safe_load(CONFIG_FRAGMENT))
        ras_rabbit = c.dependency('ras-rabbit')
        self.assertEqual(ras_rabbit['protocols'], {'amqp': {'host': '0.0.0.0'}, 'other': {'host': '1.2.3.4'}})

        # Also test the dependencies accessor
        rabbit_found = False
        for d in c.dependencies():
            if d[0] == 'ras-rabbit':
                self.assertEqual(d[1]['protocols'], {'amqp': {'host': '0.0.0.0'}, 'other': {'host': '1.2.3.4'}})
                rabbit_found = True

        self.assertTrue(rabbit_found)

    @patch('ras_backstage.ras_config.ras_config.getenv', new_callable=MockGetenv)
    def test_cf_config_falls_back_to_yaml_values(self, _):
        c = ras_config.make(yaml.safe_load(CONFIG_FRAGMENT))
        ras_postgres = c.dependency('ras-postgres')
        self.assertEqual(ras_postgres['schema'], 'my-schema')

    @patch('ras_backstage.ras_config.ras_config.getenv', new_callable=MockGetenv)
    def test_feature_flag_coerces_to_boolean(self, _):
        c = ras_config.make(yaml.safe_load(CONFIG_FRAGMENT))

        expected_true = c.feature('config-bool-true')
        self.assertTrue(isinstance(expected_true, bool))
        self.assertTrue(expected_true)

        expected_true = c.feature('config-true-flag')
        self.assertTrue(isinstance(expected_true, bool))
        self.assertTrue(expected_true)

        expected_false = c.feature('config-false-flag')
        self.assertTrue(isinstance(expected_true, bool))
        self.assertFalse(expected_false)

        expected_false = c.feature('config-nonexistent-flag')
        self.assertTrue(isinstance(expected_true, bool))
        self.assertFalse(expected_false)
