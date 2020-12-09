#!/usr/bin/env python3
#
"""
Basic RabbitMQ test tool.

Can be configured as producer or consumer.

Producer sends a configurable payload to an exchange.

Consumer reads form a queue and output the result to stdout.
"""

import sys
import os
import time

import pika
import json
import yaml

import rbmq_config
# from rbmq_config import Config

def get_connection_parameters(config):
    """
    Build pika connection parameters from config.
    
    Parameter: 
        config: Config object.

    Returns:
        The pika connection parameters.
    """
    conn_credentials = pika.PlainCredentials(config["user"], config["pw"])
    conn_parameters = pika.ConnectionParameters(config["host"],
                                       config["port"],
                                       config["vhost"],
                                       conn_credentials)
    return conn_parameters

def default_playload():
    """
    Define the default hardcode payload for quick tests.
    
    Returns:
        A default payload with the current time.
    """
    return {
        'properties': pika.BasicProperties(
            content_type='text/plain',
            delivery_mode=1
        ),
        'body': "Now it's {} in {}".format(
                time.asctime(time.localtime()), time.tzname)
    }

def get_payload(payload_list):
    """Load the payload properties and body from file."""
    data_path = os.path.dirname(payload_list)
    with open(payload_list) as f:
        definition= yaml.safe_load(f)
    payload = {
        'properties': pika.BasicProperties(
                content_type = definition['properties']['content_type'],
                headers = definition['properties']['headers'],
                delivery_mode = 1),
        'body': get_body(
            os.path.join(data_path, definition['content']),
            definition['properties']['content_type'])
    }
    return payload

def get_body(file, type):
    """
    Load payload body from file.

    Currently only text and json filetypes are supported.

    Returns:
        Body in text or json format
    """
    body = None
    if 'text' == os.path.basename(type):
        body = get_plain_file(file)
    elif 'json' == os.path.basename(type):
        body = get_json_file(file)
    return body 

def get_plain_file(file):
    """
    Load text file.

    Returns: 
        the stringfied file
    """
    with open(file) as f:
        body = f.read()
    return body

def get_json_file(file):
    """
    Load json file.

    Returns: 
        a json string
    """
    with open(file) as f:
        data = json.load(f)
    return json.dumps(data) 

def usage():
    """Print usage to stdout."""
    print("""
    usage:
      rbmq-test produce | consume

    """
    )


def produce(config):
    """
    Send message to a RabbitMQ server.

    See rbmq_config.py for the possible parameters.
    """
    # Automatic connection recovery
    while config["endless"]:
        try:
            connection = pika.BlockingConnection(
                get_connection_parameters(config)
                )
            channel = connection.channel()
            channel.queue_declare(queue=config["queue"])
            print("MQ Producer is running, stop with CTRL-C")
            while True:
                if config["payload"]:
                    payload = get_payload(config["payload"])
                else:
                    payload = default_playload()
                channel.basic_publish(exchange=config["exchange"],
                                    routing_key = config["queue"],
                                    properties = payload['properties'],
                                    body = payload['body'])
                                    
                print(" Sent {}".format(payload))
                # Sleep x seconds so we don't flood the exchange
                if config["interval"]:
                    time.sleep(config["interval"])

            connection.close()
        # Don't recover if connection was closed by broker
        except pika.exceptions.ConnectionClosedByBroker as conn_excep:
            print("ConnectionClosedByBroker: {}".format(conn_excep))/AMQP
            //
            break
        # Don't recover on channel errors
        except pika.exceptions.AMQPChannelError as amqp_chan_err:
            print("AMQPChannelError: {}".format(amqp_chan_err))
            break
        # Break on keyboard interrupt
        except KeyboardInterrupt:
            break
        # Recover on all other connection errors
        except pika.exceptions.AMQPConnectionError:
            # Retry once a second
            print("No connection, retrying ...")
            time.sleep(1)
            continue


def consume(config):
    """
    Read from a RabbitMQ queue.

    Fetch message from a given queue in an endless loop.

    See rbmq_config.py for the possible parameters.
    """
    # queue=config["queue"],
    #        payload='',
    #         exchange=config["exchange"],
    #         endless=config["endless"]):
        # Automatic connection recovery
    while True:
        try:
            connection = pika.BlockingConnection(
                get_connection_parameters(config)
                )
            channel = connection.channel()
            channel.queue_declare(config["queue"])
            def callback(ch, method, properties, body):
                print("Received {}".format(body))

            channel.basic_consume(
                queue=config["queue"],
                on_message_callback=callback,
                auto_ack=True
            )

            print('Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()

        # Don't recover if connection was closed by broker
        except pika.exceptions.ConnectionClosedByBroker:
            break
        # Don't recover on channel errors
        except pika.exceptions.AMQPChannelError:
            break
        # Break on keyboard interrupt
        except KeyboardInterrupt:
            break
        # Recover on all other connection errors
        except pika.exceptions.AMQPConnectionError:
            # Retry once a second
            print("No connection, retrying ...")
            time.sleep(1)
            continue


if __name__ == "__main__":
    if not 2 == len(sys.argv):
        usage()
        exit(1)
    mode = sys.argv[1]
    config = rbmq_config.Config().get_config()
    # Log our configuration
    print("{} config is {}".format(mode, config))
    try:
        if 'produce' == mode:
            produce(config)
        elif 'consume'  == mode:
            consume(config)
        else:
            usage()
            exit(1)
    except KeyboardInterrupt:
        pass
