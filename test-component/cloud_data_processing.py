#!/usr/bin/env python3
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import re
import xml.etree.ElementTree as ET
# db_client = InfluxDBClient('188.166.238.158', 32485, 'root', 'root', 'k8s')
db_client = InfluxDBClient('monitoring-influxdb', 8086, 'root', 'root', 'k8s')
CONFIG_PATH = ''
ITEM_PATH = 'items.cfg'

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
    json_body = [
        {
            "measurement": "data_collect_rate",
            "tags": {
                "topic_id": str(msg.topic)
            },
            "fields": {
                "num_of_message": 1,
                "value": data
            }
        }
    ]
    db_client.write_points(json_body)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# client.connect("188.166.238.158", 30146, 60)
client.connect("mqtt-service", 1883, 60)

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
# 2017-03-27T16:48:10.756300242Z </obj>

# <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
# 2017-03-27T16:52:26.592544615Z                 <obj>
# 2017-03-27T16:52:26.592554992Z                     <int val="81" name="data"/>
# 2017-03-27T16:52:26.592564915Z                 </obj>

