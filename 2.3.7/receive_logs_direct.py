#!/usr/bin/env python
import os
import sys
import time

import pika
import dotenv

dotenv.load_dotenv('../.env')
HOST = os.environ.get('AMQP_HOST')
# PORT = int(os.environ.get('AMQP_PORT'))
USERNAME = os.environ.get('AMPQ_USERNAME')
PASSWORD = os.environ.get('AMPQ_PASSWORD')

def main():
    credentials = pika.PlainCredentials(username=USERNAME, password=PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    severities = sys.argv[1:]

    if not severities:
        sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        sys.exit(1)

    for severity in severities:
        channel.queue_bind(
            exchange='direct_logs', queue=queue_name, routing_key=severity)
    print(' [*] Waiting for logs. To exit press CTRL+C')


    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
                os._exit(0)
