"""Configuration module for RBMQ tester."""
import os
import sys

import yaml


class Config:
    """
    Configuration dictonary with default values.

    Can be overwritten by a configuration file or by environment settings.
    """
    parameters = {
        'host': 'localhost',
        'port': 5672,
        'ssl_port': 5671,
        'user': 'guest',
        'pw': 'guest',
        'vhost': 'local',
        'exchange': 'myExchg',
        'queue': 'myMQ',
        'routing_key': '',
        'endless': True,
        'payload': '',
        'interval': 0,
        'ssl_enabled': True,
        'mode': 'consume'
    }

    def __init__(self, config_file='./rbmq-config.yml'):
        """
        Construct a config object.

        Tries to load a config file. Use defaults when no file is supplied and
        the default file is not found.

        Parameters:
            config_file:
                A yaml file with configuation settings. If ommitted the config
                object will look for rbmq-tester.yml.
        """
        if config_file:
            self.load_yaml(config_file)

    def load_yaml(self, file):
        """
        Open and load configuration file.

        Overwrite and append default from the configuration file
        in YAML format.
        Do nothing if config file does not exists or load operations fails.
        """
        try:
            config_stream = open(file, 'r', encoding="utf-8")
            ext_config = yaml.safe_load(config_stream)
            # QQQ merge config
            for key in iter(ext_config.keys()):
                self.parameters[key] = ext_config[key]

        except IOError as io_err:
            print(f"Can't read configuration file {file}, throws {io_err}", \
                file=sys.stderr)

    def get_config(self):
        """
        Retrieve all settings.

        Finally overwrite default configuration with environment if set.
        If no ENV variable is set, the existing value is retained.
        """
        self.parameters["host"] = os.getenv('RBMQ_HOST',
                                        self.parameters["host"])
        self.parameters["port"] = int(os.getenv(
                                    'RBMQ_PORT',
                                    str(self.parameters["port"])))
        self.parameters["ssl_port"] = int(os.getenv(
                                        'RBMQ_SSL_PORT',
                                        str(self.parameters["ssl_port"])))
        self.parameters["user"] = os.getenv('RBMQ_USER',
                                        self.parameters["user"])
        self.parameters["pw"] = os.getenv('RBMQ_PASS',
                                      self.parameters["pw"])
        self.parameters["vhost"] = os.getenv('RBMQ_VHOST',
                                         self.parameters["vhost"])
        self.parameters["queue"] = os.getenv('RBMQ_QUEUE',
                                         self.parameters["queue"])
        self.parameters["routing_key"] = os.getenv('RBMQ_ROUTING_KEY',
                                               self.parameters["routing_key"])
        self.parameters["exchange"] = os.getenv('RBMQ_EXCHANGE',
                                            self.parameters["exchange"])
        self.parameters["payload"] = os.getenv('RBMQ_PAYLOAD',
                                           self.parameters["payload"])
        self.parameters["interval"] = int(os.getenv(
                                        'RBMQ_INTERVAL',
                                        str(self.parameters["interval"])))
        self.parameters["ssl_enabled"] = os.getenv(
                                        'RBMQ_SSL_ENABLED',
                                        str(self.parameters["ssl_enabled"])) \
                                        .lower() in ('True', 'true')
        self.parameters["mode"] = os.getenv('MODE',
                                        self.parameters["mode"])
        return self.parameters
