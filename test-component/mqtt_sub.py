#!/usr/bin/env python3
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
# db_client = InfluxDBClient('188.166.238.158', 32485, 'root', 'root', 'k8s')
# db_client = InfluxDBClient('monitoring-influxdb', 8086, 'root', 'root', 'k8s')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    _list = list()
    for i in range(0, 100):
        # client.subscribe("sensor_{}".format(i))
        _list.append(("sensor_{}".format(i), 0))

    client.subscribe("onem2m/humidity")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    json_body = [
        {
            "measurement": "data_collect_rate",
            "tags": {
                "sensor_id": msg.topic
            },
            "fields": {
                "num_of_message": 1
            }
        }
    ]
    # db_client.write_points(json_body)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("188.166.238.158", 30146, 60)
# client.connect("mqtt-service", 1883, 60)
# client.connect("localhost", 1883, 60)
# client.connect("128.199.242.5", 31382, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
