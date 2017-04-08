#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time
# from influxdb import InfluxDBClient
from influxdb.influxdb08 import InfluxDBClient
# db_client = InfluxDBClient('188.166.238.158', 32485, 'root', 'root', 'k8s')
# db_client = InfluxDBClient('127.0.0.1', 8086, 'root', 'root', 'cadvisor')
# db_client = InfluxDBClient('monitoring-influxdb', 8086, 'root', 'root', 'k8s')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    _list = list()
    for i in range(0, 5):
    #     # client.subscribe("sensor_{}".format(i))
        _list.append(("/in{}".format(i), 0))

    client.subscribe(_list)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    # print('-----{}'.format(time.time()))
    # json_body = [
    #     {
    #         "measurement": "data_collect_rate",
    #         "tags": {
    #             "sensor_id": msg.topic
    #         },
    #         "fields": {
    #             "num_of_message": 1
    #         }
    #     }
    # ]
    # json_body = [
    #     {
    #         "name": "data_collect_rate",
    #         "columns": ["data_sensing", "sensor_id"],
    #         "points": [[int(msg.payload), str(msg.topic)]]
    #     }
    # ]
    # print(json_body)
    # db_client.write_points(json_body)

def publish_message(topic, message):
    pass

mqtt_client_2 = mqtt.Client()
mqtt_client_2.on_connect = on_connect
mqtt_client_2.on_message = on_message
# mqtt_client_2.connect("localhost", 1883, 60)
mqtt_client_2.connect("188.166.238.158", 30146, 60)

mqtt_cloud = mqtt.Client()
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqtt_client_2.loop_forever()
mqtt_cloud.loop_forever()
