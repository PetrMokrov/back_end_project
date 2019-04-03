#!/usr/bin/env python
import pika
import time

def produce_message():
    print('Starting producer')
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

    while True:
        message = yield
        if message == 'quit':
            break
        channel.basic_publish(exchange='',
                              routing_key='email-queue',
                              body=message,
                              properties=pika.BasicProperties(delivery_mode=2)
        )
        print('Sent:\t', message)

    connection.close()
    yield

if __name__ == "__main__":
    print("Producer is not a sufficient app!")
    # producer = produce_message()
    # producer.send(None)
    # for i in range(10):
    #     producer.send(str(i))
    #     time.sleep(5)
    # producer.send("quit")
