#!/usr/bin/env python3
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import re
import xml.etree.ElementTree as ET
# db_client = InfluxDBClient('188.166.238.158', 32485, 'root', 'root', 'k8s')
db_client = InfluxDBClient('monitoring-influxdb', 8086, 'root', 'root', 'k8s')
CONFIG_PATH = ''
ITEM_PATH = 'items.cfg'
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    items = [(line.rstrip('\n'), 0) for line in open(ITEM_PATH)]
    client.subscribe(items)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = re.sub('\s+', ' ', str(msg.payload.decode("utf-8")).strip())
    # print(payload)
    root = ET.fromstring(payload)
    data = int(root.find('./*[@name="data"]').attrib['val'])
    timestamp_sensor = float(root.find('./*[@name="timestamp_sensor"]').attrib['val'])
    timestamp_platform = float(root.find('./*[@name="timestamp_platform"]').attrib['val'])
    time_platform_process = float(root.find('./*[@name="time_platform_process"]').attrib['val'])
    num_of_sensor = str(root.find('./*[@name="num_of_sensor"]').attrib['val'])
    timenow = time.time() + 1.76949811
    print(timestamp_sensor)
    print(timestamp_platform)
    round_trip_1 = timestamp_platform - timestamp_sensor
    print(round_trip_1)
    round_trip_2 = timenow - timestamp_platform
    print(round_trip_2)
    round_trip_3 = round_trip_1 + round_trip_2
    json_body = [
        {
            "measurement": "data_collect_rate",
            "tags": {
                "topic_id": str(msg.topic),
                "num_of_sensor": num_of_sensor
            },
            "fields": {
                "num_of_message": 1,
                "value": data,
                "round_trip_1": round_trip_1,
                "round_trip_2": round_trip_2,
                "round_trip_3": round_trip_3,
                "time_platform_process": time_platform_process
                # "time_send_cloud": time.time()
                #
            }
        }
    ]
    db_client.write_points(json_body)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# client.connect("188.166.238.158", 30146, 60)
client.connect("mqtt-service", 1883, 60)
# client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

# <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
# 2017-03-27T16:48:10.756209294Z <obj>
# 2017-03-27T16:48:10.756215739Z     <str val="onem2m_pf_2" name="itemId"/>
# 2017-03-27T16:48:10.756221656Z     <str val="onem2m_1" name="platformId"/>
# 2017-03-27T16:48:10.756227451Z     <str val="onem2m" name="platformType"/>
# 2017-03-27T16:48:10.756233083Z     <str val="fog_1" name="clusterId"/>
# 2017-03-27T16:48:10.756238542Z     <str val="temperature" name="category"/>
# 2017-03-27T16:48:10.756287257Z     <int val="86" name="data"/>
# 2017-03-27T16:48:10.756294421Z     <str val="celsius" name="unit"/>
# 2017-03-27T16:48:10.756300242Z     <int val="423423423" name="timestamp_platform"/>
# 2017-03-27T16:48:10.756300242Z     <int val="423423423" name="timestamp_sensor"/>

# <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
# 2017-03-27T16:52:26.592544615Z                 <obj>
# 2017-03-27T16:52:26.592554992Z                     <int val="81" name="data"/>
# 2017-03-27T16:52:26.592564915Z                 </obj>

