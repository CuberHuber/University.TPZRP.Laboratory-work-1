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

credentials = pika.PlainCredentials(username=USERNAME, password=PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST, credentials=credentials))
channel = connection.channel()


channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)
print(" [x] Sent %r:%r" % (severity, message))
connection.close()
