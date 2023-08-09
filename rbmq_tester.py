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

import ssl
import json
import yaml
import certifi
import pika

import rbmq_config


def get_connection_parameters(param):
    """
    Build pika connection param from configuration.

    Parameter:
        param: Config object.

    Returns:
        The pika connection param.
    """
    conn_credentials = pika.PlainCredentials(param["user"], param["pw"])
    conn_parameters = None

    if param["ssl_enabled"]:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.verify_mode = ssl.CERT_REQUIRED
        # Load the CA certificates used for validating the peer's certificate
        context.load_verify_locations(cafile=os.path.relpath(certifi.where()),
                                      capath=None,
                                      cadata=None)
        conn_parameters = pika.ConnectionParameters(
            host=param["host"],
            port=param["ssl_port"],
            virtual_host=param["vhost"],
            ssl_options=pika.SSLOptions(context),
            credentials=conn_credentials
            )
    else:
        conn_parameters = pika.ConnectionParameters(
            host=param["host"],
            port=param["port"],
            virtual_host=param["vhost"],
            credentials=conn_credentials
            )

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
        'body': f"Now it's {time.asctime(time.localtime())} in {time.tzname}"
    }


def get_payload(payload_list):
    """Load the payload properties and body from file."""
    data_path = os.path.dirname(payload_list)
    with open(payload_list, encoding="utf-8") as file:
        definition = yaml.safe_load(file)
    payload = {
        'properties': pika.BasicProperties(
                content_type=definition['properties']['content_type'],
                headers=definition['properties']['headers'],
                delivery_mode=1),
        'body': get_body(
            os.path.join(data_path, definition['content']),
            definition['properties']['content_type'])
    }
    return payload


def get_body(file, content_type):
    """
    Load payload body from file.

    Currently only text and json filetypes are supported.

    Returns:
        Body in text or json format
    """
    body = None
    if 'text' == os.path.basename(content_type):
        body = get_plain_file(file)
    elif 'json' == os.path.basename(content_type):
        body = get_json_file(file)
    return body


def get_plain_file(file):
    """
    Load text file.

    Returns:
        the stringfied file
    """
    with open(file, encoding="utf-8") as file:
        body = file.read()
    return body


def get_json_file(file):
    """
    Load json file.

    Returns:
        a json string
    """
    with open(file, encoding="utf-8") as file:
        data = json.load(file)
    return json.dumps(data)


def publish(channel, exch, queue, key, load, vhost):
    """
    Publish payload to message queue.
    Use a connection channel to send the payload to a
    a queue on a given exchange.
    """

    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(exchange=exch,
                    routing_key=key,
                    properties=load['properties'],
                    body=load['body'])
    print(f" Sent {load} to {exch} on {vhost}")


def usage():
    """Print usage to stdout."""
    print("""
    usage:
      rbmq-test produce | consume

    """)


def produce(param):
    """
    Send message to a RabbitMQ server.

    See rbmq_config.py for the possible parameters.
    """
    # Automatic connection recovery
    while param["endless"]:
        try:
            connection = pika.BlockingConnection(
                get_connection_parameters(param)
                )
            # channel = connection.channel()
            # channel.queue_declare(queue=param["queue"], durable=True)
            # Prepare payload
            if param["payload"]:
                payload = get_payload(param["payload"])
            else:
                payload = default_playload()
            # Check / prepare param
            routing_key = param["routing_key"] \
                if param["routing_key"] else param["queue"]
            print("MQ Producer is running, stop with CTRL-C")
            while True:
                publish(
                    connection.channel(),
                    param["exchange"],
                    param["queue"],
                    routing_key,
                    payload,param['vhost']
                )
                # channel.basic_publish(exchange=param["exchange"],
                #                       routing_key=routing_key,
                #                       properties=payload['properties'],
                #                       body=payload['body'])
                # print(f" Sent {payload} to {param['exchange']} on {param['vhost']}")
                # Sleep x seconds so we don't flood the exchange
                if param["interval"]:
                    time.sleep(param["interval"])

            # connection.close()
        # Don't recover if connection was closed by broker
        except pika.exceptions.ConnectionClosedByBroker as conn_excep:
            print(f"ConnectionClosedByBroker: {conn_excep}")
            break
        # Don't recover on channel errors
        except pika.exceptions.AMQPChannelError as amqp_chan_err:
            print(f"AMQPChannelError: {amqp_chan_err}")
            connection.close()
            break
        # Break on keyboard interrupt
        except KeyboardInterrupt:
            connection.close()
            break
        # Recover on all other connection errors
        except pika.exceptions.AMQPConnectionError as amqp_conn_err:
            # Retry once a second
            print(f"{amqp_conn_err}. No connection, retrying ...")
            time.sleep(1)
            continue


def consume(param):
    """
    Read from a RabbitMQ queue.

    Fetch message from a given queue in an endless loop.

    See rbmq_config.py for the possible parameters.
    """
    while True:
        try:
            connection = pika.BlockingConnection(
                get_connection_parameters(param)
                )
            channel = connection.channel()
            channel.queue_declare(param["queue"], durable=True)

            def callback(channel, method, properties, body):
                print(f"Received {body}")

            channel.basic_consume(
                queue=param["queue"],
                on_message_callback=callback,
                auto_ack=True
            )

            print('Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()

        # Don't recover if connection was closed by broker
        except pika.exceptions.ConnectionClosedByBroker as conn_excep:
            print(f"ConnectionClosedByBroker: {conn_excep}")
            break
        # Don't recover on channel errors
        except pika.exceptions.AMQPChannelError as amqp_chan_err:
            print(f"AMQPChannelError: {amqp_chan_err}")
            break
        # Break on keyboard interrupt
        except KeyboardInterrupt:
            break
        # Recover on all other connection errors
        except pika.exceptions.AMQPConnectionError as amqp_conn_err:
            # Retry once a second
            print(f"{amqp_conn_err}. No connection, retrying ...")
            time.sleep(1)
            continue


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    MODE = sys.argv[1]
    parameters = rbmq_config.Config().get_config()
    # Log our configuration
    print(f"{MODE} config is {parameters}")
    try:
        if 'produce' == MODE:
            parameters['mode'] = MODE
            produce(parameters)
        elif 'consume' == MODE:
            parameters['mode'] = MODE
            consume(parameters)
        else:
            usage()
            sys.exit(1)
    except KeyboardInterrupt:
        pass
