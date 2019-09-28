#!/usr/bin/env python3
#
import os
import time

import pika
import yaml

from mq_config import config

# # Default configuration
# # Using vhost / and user guest
# # Overridden by configuration file when exists
# config = {
#     'host': 'localhost',
#     'port': 5672,
#     'user': 'guest',
#     'pw': 'guest',
#     'vhost': '/testing',
#     'queue': 'hello-MQ',
#     'endless': True
# }
# config_file = './mq_test.yml'

# env_parameters = {
#     'host': 'RBMQ_HOST',
#     'port': 'RBMQ_PORT',
#     'user': 'RBMQ_USER',
#     'pw': 'RBMQ_PASS',
#     'vhost': 'RBMQ_VHOST',
#     'exchange': 'RBMQ_EXCHG',
#     'queue': 'RBMQ_QUEUE'
# }

# # Load configuration file
# try:
#     config_stream = open(config_file, 'r')
#     ext_config = yaml.safe_load(config_stream)
#     # QQQ merge config
#     for key in iter(ext_config.keys()):
#         config[key] = ext_config[key]
    
# except:
#     print("Can't read configuration file {}".format(config_file))

# # Overwrite configuration with environment
# config["host"] = os.getenv('RBMQ_HOST', config["host"])
# print("Set host from environment.")
# # if os.environ['RBMQ_USER']:
# config["user"] = os.getenv('RBMQ_USER', config["user"])
# print("Set user from environment.")

print("Config is {}".format(config))

# def load_environ(env_name):
#     value = ''
#     if os.environ[env_name]:
#         value = os.environ[env_name]
#         print("Set {} from environment.".format(value))
#     return value


# Load configuration file
# First try to load the ./mq_test.yml
# next check if any environment variables are set.
# for key in iter(env_parameters.keys()):
#     print("key: {}; value: {}".format(key, env_parameters[key]))
#     env_value = load_environ(env_parameters[key])
#     if env_value:



# Set connection parameters
conn_credentials = pika.PlainCredentials(config["user"], config["pw"])
# conn_credentials = pika.PlainCredentials('rbmq_user', 'rbmq_pass')
conn_parameters = pika.ConnectionParameters(config["host"],
                                       config["port"],
                                       config["vhost"],
                                       conn_credentials)
# conn_parameters = pika.ConnectionParameters('localhost',
#                                             5672,
#                                             '/testing',
#                                             conn_credentials)

# Load payload file if exists

# ToDo: define payload handling

def produce(queue = config["queue"],
            payload = '',
            exchange = config["exchange"],
            endless = config["endless"]):
    connection = pika.BlockingConnection(conn_parameters)
    channel = connection.channel()
    channel.queue_declare(queue=config["queue"])
    print("MQ Producer is running, stop with CTRL-C")
    while True:
        if not payload:
            payload = "Now it's {} in {}".format(
                        time.asctime(time.localtime()), time.tzname)

        channel.basic_publish(exchange=exchange,
                            routing_key = queue,
                            body = payload)
                            
        print(" Sent {}".format(payload))
        # Sleep 5 seconds so we don't flood the exchange
        time.sleep(5)

    connection.close()

if __name__ == "__main__":
    try:
        produce()
    except KeyboardInterrupt:
        pass
