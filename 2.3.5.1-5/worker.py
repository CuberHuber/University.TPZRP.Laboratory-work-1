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
    channel.basic_qos(prefetch_count=1)
    channel.queue_declare(queue='task_queue', durable=True)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        # Добавляем ответ
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # убрали автоответ
    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
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
