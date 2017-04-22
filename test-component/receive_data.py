#!/usr/bin/env python
import pika
import os

fog_broker_host = os.environ.get('FOG_BROKER_HOST')
fog_broker_port = os.environ.get('FOG_BROKER_PORT')
fog_broker_auth = os.environ.get('FOG_BROKER_AUTH')
fog_username = fog_broker_auth.split(':')[0]
fog_password = fog_broker_auth.split(':')[1]
# Connect to fog broker service
credentials = pika.PlainCredentials(fog_username, fog_password)
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=fog_broker_host, port=int(fog_broker_port), credentials=credentials))
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
    forward_message(body)

def forward_message(body):
    _cloud_broker_host = os.environ.get('CLOUD_BROKER_HOST')
    _cloud_broker_port = os.environ.get('CLOUD_BROKER_PORT')
    _cloud_broker_auth = os.environ.get('CLOUD_BROKER_AUTH')
    _cloud_username = _cloud_broker_auth.split(':')[0]
    _cloud_password = _cloud_broker_auth.split(':')[1]
    #
    _credentials = pika.PlainCredentials(_cloud_username, _cloud_password)
    _connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=_cloud_broker_host, port=int(_cloud_broker_port), credentials=_credentials))
    _channel = _connection.channel()
    _channel.exchange_declare(exchange='sensor_collector',
                             exchange_type='fanout')

    message = body
    _channel.basic_publish(exchange='sensor_collector',
                          routing_key='',
                          body=message)
    print(" [x] Sent fallback %r" % message)
    _connection.close()

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()