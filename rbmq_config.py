#
# Configuration module for RBMQ tester
#
import os
import sys

import yaml

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
    'interval': None
}

config_file = './rbmq-tester.yml'


# Overwrite and append default from the configuration file
# in YAML format.
# Do nothing if config file does not exists or load operations fails.
def load_yaml(file):
    try:
        config_stream = open(file, 'r')
        ext_config = yaml.safe_load(config_stream)
        # QQQ merge config
        for key in iter(ext_config.keys()):
            config[key] = ext_config[key]

    except:
        print("Can't read configuration file {}".format(config_file), file=sys.stderr)

# Load confguration file if exists.
load_yaml(config_file)

# Finally overwrite configuration with environment
# If no ENV variable is set, the existing value is retained.
config["host"] = os.getenv('RBMQ_HOST', config["host"])
config["user"] = os.getenv('RBMQ_USER', config["user"])
config["pw"] = os.getenv('RBMQ_PASS', config["pw"])
config["queue"] = os.getenv('RBMQ_QUEUE', config["queue"])
config["exchange"] = os.getenv('RBMQ_EXCHG', config["exchange"])
config["payload"] = os.getenv('RBMQ_PAYLOAD', config["payload"])
config["interval"] = int(os.getenv('RBMQ_INTERVAL', config["interval"]))
