#!/usr/bin/env python
import pika
import os

cloud_broker_host = os.environ.get('CLOUD_BROKER_HOST')
cloud_broker_port = os.environ.get('CLOUD_BROKER_PORT')
cloud_broker_auth = os.environ.get('CLOUD_BROKER_AUTH')
cloud_username = cloud_broker_auth.split(':')[0]
cloud_password = cloud_broker_auth.split(':')[1]
# Connect to fog broker service
credentials = pika.PlainCredentials(cloud_username, cloud_password)
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=cloud_broker_host, port=int(cloud_broker_port), credentials=credentials))
channel = connection.channel()
channel.exchange_declare(exchange='sensor_collector',
                         exchange_type='fanout')
#
result = channel.queue_declare(durable=True, exclusive=False)
queue_name = result.method.queue

channel.queue_bind(exchange='sensor_collector',
                   queue=queue_name)

print(' [*] Waiting for data. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()