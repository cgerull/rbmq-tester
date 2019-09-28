#!/usr/bin/env python3
#
import os
import time

import pika
import yaml

from mq_config import config

# Log our configuration
print("Config is {}".format(config))

# Set connection parameters
conn_credentials = pika.PlainCredentials(config["user"], config["pw"])
conn_parameters = pika.ConnectionParameters(config["host"],
                                       config["port"],
                                       config["vhost"],
                                       conn_credentials)

# ToDo: define payload handling


def produce(queue = config["queue"],
            payload = '',
            exchange = config["exchange"],
            endless = config["endless"]):
    # Automatic connection recovery
    while True:
        try:
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
            continue


if __name__ == "__main__":
    try:
        produce()
    except KeyboardInterrupt:
        pass
