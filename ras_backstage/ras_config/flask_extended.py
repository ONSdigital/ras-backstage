from flask import Flask as BaseFlask, Config as BaseConfig


class Config(BaseConfig):
    """Flask config enhanced with a `from_yaml` method."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dependency = {}
        self.feature = {}

    def from_ras_config(self, config):
        for k, v in config.items():
            self[k] = v

        for k, v in config.dependencies():
            self.dependency[k] = v

        self.feature = config.features()


class Flask(BaseFlask):
    """Extended version of `Flask` that implements custom config class"""

    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return Config(root_path, self.default_config)
