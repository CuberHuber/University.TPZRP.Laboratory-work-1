#!/usr/bin/env python
import os
import sys

import pika
import dotenv

dotenv.load_dotenv('../.env')
HOST = os.environ.get('AMQP_HOST')
# PORT = os.environ.get('AMQP_PORT')
USERNAME = os.environ.get('AMPQ_USERNAME')
PASSWORD = os.environ.get('AMPQ_PASSWORD')

credentials = pika.PlainCredentials(username=USERNAME, password=PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST, credentials=credentials))

channel = connection.channel()
channel.queue_declare(queue='hello')
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)
print(" [x] Sent %r" % message)
connection.close()
