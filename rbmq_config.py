"""Configuration module for RBMQ tester."""
import os
import sys

import yaml


class Config:
    """
    Configuration dictonary with default values.

    Can be overwritten by a configuration file or by environment settings.
    """
    config = {
        'host': 'localhost',
        'port': 5672,
        'ssl_port': 5671,
        'user': 'guest',
        'pw': 'guest',
        'vhost': 'LOCAL',
        'exchange': 'myExchg',
        'queue': 'myMQ',
        'routing_key': '',
        'endless': True,
        'payload': '',
        'interval': 0,
        'ssl_enabled': True,
        'mode': 'consume'
    }

    def __init__(self, config_file='./rbmq-tester.yml'):
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
            config_stream = open(file, 'r')
            ext_config = yaml.safe_load(config_stream)
            # QQQ merge config
            for key in iter(ext_config.keys()):
                self.config[key] = ext_config[key]

        except:
            print("Can't read configuration file {}".format(file),
                  file=sys.stderr)

    def get_config(self):
        """
        Retrieve all settings.

        Finally overwrite default configuration with environment if set.
        If no ENV variable is set, the existing value is retained.
        """
        self.config["host"] = os.getenv('RBMQ_HOST',
                                        self.config["host"])
        self.config["port"] = int(os.getenv('RBMQ_PORT',
                                            self.config["port"]))
        self.config["ssl_port"] = int(os.getenv('RBMQ_SSL_PORT',
                                                self.config["ssl_port"]))
        self.config["user"] = os.getenv('RBMQ_USER',
                                        self.config["user"])
        self.config["pw"] = os.getenv('RBMQ_PASS',
                                      self.config["pw"])
        self.config["vhost"] = os.getenv('RBMQ_VHOST',
                                         self.config["vhost"])
        self.config["queue"] = os.getenv('RBMQ_QUEUE',
                                         self.config["queue"])
        self.config["routing_key"] = os.getenv('RBMQ_ROUTING_KEY',
                                               self.config["routing_key"])
        self.config["exchange"] = os.getenv('RBMQ_EXCHANGE',
                                            self.config["exchange"])
        self.config["payload"] = os.getenv('RBMQ_PAYLOAD',
                                           self.config["payload"])
        self.config["interval"] = int(os.getenv('RBMQ_INTERVAL',
                                                self.config["interval"]))
        self.config["ssl_enabled"] = (os.getenv('RBMQ_SSL_ENABLED',
                                                self.config["ssl_enabled"]))
        self.config["mode"] = os.getenv('MODE',
                                        self.config["mode"])
        return self.config
