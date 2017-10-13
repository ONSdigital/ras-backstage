import json
from os import getenv

import yaml
from structlog import get_logger

log = get_logger()


def map_dict(d, key_mapper=None, value_mapper=None):
    def ident(x):
        return x
    key_mapper = key_mapper or ident
    value_mapper = value_mapper or ident
    return {key_mapper(k): value_mapper(v) for k, v in d.items()}


def lower_keys(d):
    return map_dict(d, key_mapper=str.lower)


class RasDependencyError(Exception):
    pass


class DependencyProxy:

    def __init__(self, dependency, name, overrides=None):
        self._dependency = lower_keys(dependency)
        self._name = name
        self._overrides = overrides or {}

    def __getattr__(self, item):
        return self[item]

    def __getitem__(self, item):
        k = "{}.{}".format(self._name, item)
        return self._overrides.get(item) or getenv(k) or self._dependency[item]


class FeaturesProxy:

    def __init__(self, features):
        self._features = features

    def __getattr__(self, item):
        return self[item]

    def __getitem__(self, item):
        k = "feature.{}".format(item)
        result = getenv(k) or self._features.get(item)
        try:
            return result.lower() in ('true', 't', 'yes', 'y', '1')
        except AttributeError:
            return result is True


class RasConfig:
    def __init__(self, config_data):
        self.service = {k: getenv(k, v) for k, v in config_data['service'].items()}
        self._dependencies = lower_keys(config_data.get('dependencies', {}))
        self._features = FeaturesProxy(config_data.get('features', {}))

    def feature(self, name):
        return self._features[name]

    def items(self):
        return self.service.items()

    def dependency(self, k):
        try:
            return DependencyProxy(self._dependencies[k], k)
        except KeyError:
            raise RasDependencyError("Dependency with name '{}' not found.".format(k))

    def dependencies(self):
        return {k: self.dependency(k) for k in self._dependencies.keys()}.items()

    def features(self):
        return self._features


class CloudFoundryServices:
    def __init__(self, service_data):
        self._lookup = {v['name']: v['credentials']
                        for service_config in service_data.values()
                        for v in service_config}

    def get(self, svc_name):
        result = self._lookup[svc_name]
        return result


class RasCloudFoundryConfig(RasConfig):

    def __init__(self, config_data):
        super().__init__(config_data)

        vcap_services = json.loads(getenv('VCAP_SERVICES'))
        self._services = CloudFoundryServices(vcap_services)

    def dependency(self, k):
        try:
            return DependencyProxy(self._dependencies[k], k, overrides=self._services.get(k))
        except KeyError:
            return super().dependency(k)


def make(config_data):
    vcap_application = getenv('VCAP_APPLICATION')
    if vcap_application:
        # log.info("CloudFoundry detected. Creating CloudFoundry configuration object.")
        return RasCloudFoundryConfig(config_data)
    else:
        # log.info("CloudFoundry not detected. Creating standard configuration object.")
        return RasConfig(config_data)


def from_yaml_file(path):
    with open(path) as f:
        data = yaml.safe_load(f.read())

    return make(data)
