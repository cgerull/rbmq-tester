#!/usr/bin/env python3
#
import sys
import time

import pika

from rbmq_config import config

# Set connection parameters
conn_credentials = pika.PlainCredentials(config["user"], config["pw"])
conn_parameters = pika.ConnectionParameters(config["host"],
                                       config["port"],
                                       config["vhost"],
                                       conn_credentials)

# ToDo: define payload handling
def get_payload(file):
    pass

def usage():
    print("""
    usage:
      rbmq-test produce | consume

    """
    )


def produce(queue = config["queue"],
            payload_file=config["payload"],
            exchange = config["exchange"],
            endless = config["endless"],
            interval = config["interval"]):
    if payload_file:
        payload = get_payload(payload_file)
    
    # Automatic connection recovery
    while True:
        try:
            connection = pika.BlockingConnection(conn_parameters)
            channel = connection.channel()
            channel.queue_declare(queue=queue)
            print("MQ Producer is running, stop with CTRL-C")
            while True:
                if not payload_file:
                    payload = "Now it's {} in {}".format(
                                time.asctime(time.localtime()), time.tzname)

                channel.basic_publish(exchange=exchange,
                                    routing_key = queue,
                                    body = payload)
                                    
                print(" Sent {}".format(payload))
                # Sleep x seconds so we don't flood the exchange
                if interval:
                    time.sleep(interval)

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
            # Retry once a second
            print("No connection, retrying ...")
            time.sleep(1)
            continue


def consume(queue=config["queue"],
            payload='',
            exchange=config["exchange"],
            endless=config["endless"]):
        # Automatic connection recovery
        while True:
            try:
                connection = pika.BlockingConnection(conn_parameters)
                channel = connection.channel()
                channel.queue_declare(queue=queue)
                def callback(ch, method, properties, body):
                    print("Received {}".format(body))

                channel.basic_consume(
                    queue=queue,
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
    # Log our configuration
    print("{} config is {}".format(mode, config))
    try:
        if 'produce' == mode:
            produce()
        elif 'consume'  == mode:
            consume()
        else:
            usage()
            exit(1)
    except KeyboardInterrupt:
        pass
