#!/usr/bin/env python
import pika
import os
import time

broker_service_host = os.environ.get('FOG_BROKER_HOST')
broker_service_port = os.environ.get('FOG_BROKER_PORT')
broker_service_auth = os.environ.get('FOG_BROKER_AUTH')
username = broker_service_auth.split(':')[0]
password = broker_service_auth.split(':')[1]
#
credentials = pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=broker_service_host, port=int(broker_service_port), credentials=credentials))
channel = connection.channel()
channel.exchange_declare(exchange='sensor_collector',
                         exchange_type='fanout')
#
consequence_number = 0
while True:
    message = 'number: '+str(consequence_number)
    channel.basic_publish(exchange='sensor_collector',
                          routing_key='',
                          body=message)
    print(" [x] Sent %r" % message)
    consequence_number += 1
    time.sleep(10)
connection.close()