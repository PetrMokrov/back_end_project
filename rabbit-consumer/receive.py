#!/usr/bin/env python
import pika
import traceback, sys
import time

print('Starting consumer')
conn_params = pika.ConnectionParameters('rabbit', 5672, socket_timeout=10)
while True:
    try:
        connection = pika.BlockingConnection(conn_params)
        break
    except pika.exceptions.AMQPConnectionError:
        print('Cannot connect yet, sleeping 3 seconds')
        time.sleep(3)
channel = connection.channel()
print('Connection successful')

channel.queue_declare(queue='email-queue', durable=True)

def callback(channel, method, properties, body):
    print('Received\t', body.decode())
    # insert sending e-mail here
    channel.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(callback, queue='email-queue')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
except Exception:
    channel.stop_consuming()
    traceback.print_exc(file=sys.stdout)
