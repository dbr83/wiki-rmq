#!/usr/bin/env python
import pika, os, random, csv, time

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE')
RABBITMQ_ROUTING_KEY = os.getenv('RABBITMQ_ROUTING_KEY')
RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE')
CSV_FILE = os.getenv('CSV_FILE')

while True:
    try:
       connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
       break
    except:
       print("Connection to RabbitMQ failed. Retrying connection in 5 seconds.")
       time.sleep(5)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=RABBITMQ_QUEUE)
channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='direct')

with open(CSV_FILE, 'r') as csvfile:
    datareader = csv.reader(csvfile)

    for row in datareader:
        line = ',,,'.join(row)
        time.sleep(random.uniform(0, 1))
        print(f"Sending {line}")
        channel.basic_publish(exchange=RABBITMQ_EXCHANGE, routing_key=RABBITMQ_ROUTING_KEY, body=line)

connection.close()

