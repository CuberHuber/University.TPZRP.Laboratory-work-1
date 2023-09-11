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


channel.exchange_declare(exchange='logs', exchange_type='fanout')
message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(" [x] Sent %r" % message)
connection.close()
