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


channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)

print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()
