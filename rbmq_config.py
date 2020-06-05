#
# Configuration module for RBMQ tester
#
import os
import sys

import yaml

class Config:
# Configuration dictonary with default values.
# Can be overwritten by configuration file or by environment settings.
    config = {
        'host': 'localhost',
        'port': 5672,
        'user': 'guest',
        'pw': 'guest',
        'vhost': '/testing',
        'exchange': '',
        'queue': 'hello-MQ',
        'endless': True,
        'payload': '',
        'interval': 0
    }

    #config_file = './rbmq-tester.yml'

    def __init__(self, config_file='./rbmq-tester.yml'):
        if config_file:
            self.load_yaml(config_file)

    # Overwrite and append default from the configuration file
    # in YAML format.
    # Do nothing if config file does not exists or load operations fails.
    def load_yaml(self,file):
        try:
            config_stream = open(file, 'r')
            ext_config = yaml.safe_load(config_stream)
            # QQQ merge config
            for key in iter(ext_config.keys()):
                self.config[key] = ext_config[key]

        except:
            print("Can't read configuration file {}".format(file), file=sys.stderr)

    def get_config(self):
        # Finally overwrite configuration with environment
        # If no ENV variable is set, the existing value is retained.
        self.config["host"] = os.getenv('RBMQ_HOST', self.config["host"])
        self.config["port"] = int(os.getenv('RBMQ_PORT', self.config["port"]))
        self.config["user"] = os.getenv('RBMQ_USER', self.config["user"])
        self.config["pw"] = os.getenv('RBMQ_PASS', self.config["pw"])
        self.config["vhost"] = os.getenv('RBMQ_VHOST', self.config["vhost"])
        self.config["queue"] = os.getenv('RBMQ_QUEUE', self.config["queue"])
        self.config["exchange"] = os.getenv('RBMQ_EXCHANGE', self.config["exchange"])
        self.config["payload"] = os.getenv('RBMQ_PAYLOAD', self.config["payload"])
        self.config["interval"] = int(os.getenv('RBMQ_INTERVAL', self.config["interval"]))
        return self.config
