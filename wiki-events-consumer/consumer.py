#!/usr/bin/env python
import pika, os, time
from io import StringIO 
from datetime import datetime

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE')
RABBITMQ_ROUTING_KEY = os.getenv('RABBITMQ_ROUTING_KEY')
RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE')
OUTPUT_FILE = os.getenv('OUTPUT_FILE')

wiki_count = 0
dewiki_count = 0
t1 = datetime.now()

def consume_callback(ch, method, properties, body):
    global wiki_count, dewiki_count, t1
    try:
        t2 = datetime.now()
        delta = t2-t1
        if delta.total_seconds() >= 60:
            edits = f"Between {t1} and {t2} there were {wiki_count} global edits and {dewiki_count} German edits on Wikipedia.\n"
            print(edits)
            f = open(OUTPUT_FILE, "a")
            f.write(edits)
            f.close()
            wiki_count = 0
            dewiki_count = 0
            t1 = datetime.now()
    except Exception as error:
        print("An exception occurred:", error)

    row = body.decode().split(",,,")
    if row[3] == 'edit':
        wiki_count += 1
        if row[15] == 'dewiki':
            dewiki_count += 1

while True:
    try:
       params = pika.ConnectionParameters(host=RABBITMQ_HOST, heartbeat=10)
       connection = pika.BlockingConnection(params)
       break
    except:
       print("Connection to RabbitMQ failed. Retrying connection in 5 seconds.")
       time.sleep(5)

channel = connection.channel()
channel.queue_declare(queue=RABBITMQ_QUEUE)
channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='direct')
channel.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE)

channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=consume_callback, auto_ack=True)
channel.start_consuming()

connection.close()

