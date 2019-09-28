#!/usr/bin/env python3
#
import pika

host = 'localhost'
port = 5672
user = 'rbmq_user'
pw = 'rbmq_pass'
vhost = '/testing'
my_queue = 'hello-MQ'

credentials = pika.PlainCredentials(user, pw)
parameters = pika.ConnectionParameters(host,
                                       port,
                                       vhost,
                                       credentials)

connection = pika.BlockingConnection(parameters)
    # pika.ConnectionParameters(host))
channel = connection.channel()

channel.queue_declare(queue=my_queue)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(
    queue = my_queue,
    on_message_callback = callback,
    auto_ack = True
)
                    
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
