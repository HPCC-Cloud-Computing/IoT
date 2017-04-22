import time
import random
import paho.mqtt.client as mqtt
import threading
import math
from influxdb.influxdb08 import InfluxDBClient

data_queue = list()
_start_time = time.time()
_before_value = 0
db_client = InfluxDBClient('127.0.0.1', 8086, 'root', 'root', 'cadvisor')

def write_file(data, file_name='log'):
    with open(file_name, "a") as myfile:
        myfile.write(data + '\n')

def push_to_db(field, data):
    json_body = [
        {
            "name": "data_collect_rate",
            "columns": ['value', 'field'],
            "points": [[int(data), field]]
        }
    ]
    db_client.write_points(json_body)

def onConnect(client, userdata, flags, rc):
    client.subscribe('test')

def onMessage(client, userdata, msg):
    # global _start_time
    # _next_time = time.time()
    # mean_value = 0
    # data_queue.append(int(msg.payload))
    # print('Pull data: {}'.format(msg.payload))
    # current_value = data_queue.pop()
    # if _next_time - _start_time == 5:
    #     temp = 0
    #     for item in data_queue:
    #         temp += item
    #     mean_value = temp / len(data_queue)
    #     data_queue.clear()
    # if _next_time - _start_time > 5:
    #     if math.fabs(current_value - mean_value) / math.fabs(_next_time - 5) > 0.2:
    #         print('Push data to cloud: {}'.format(current_value))
    # _start_time = _next_time

    global _start_time
    global _before_value
    _next_time = time.time()
    current_value = int(msg.payload)
    if math.fabs(current_value - _before_value) / math.fabs(_next_time - _start_time) > 0.2:
        print('Push data to cloud: {}'.format(current_value))
        # write_file(data='Push data to cloud: {}'.format(current_value))
        push_to_db(field='out', data=5)
        _before_value = current_value
        _start_time = _next_time

class ReceiverThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.data_queue = list()

    def run(self):
        client = mqtt.Client('sub')
        client.on_connect = onConnect
        client.on_message = onMessage
        client.connect("localhost", 1883, 60)
        client.loop_forever()


time_data_change_period = 60
time_data_change = time.time()
data_value = random.randint(0, 100)
thread = ReceiverThread()
thread.start()
client_pub = mqtt.Client('pub')
client_pub.connect('localhost', 1883)

# thread.run()
while 1:
    next_time = time.time()
    if next_time - time_data_change >= time_data_change_period:
        time_data_change_period = random.randint(10, 60)
        time_data_change = next_time
        data_value = random.randint(0, 100)
        print('Change data value. Period {} Value {}'.format(time_data_change_period, data_value))
    print('Push data to platform: {}'.format(data_value))
    # write_file(data='Push data to platform: {}'.format(data_value))
    push_to_db(field='in', data=data_value)
    client_pub.publish(topic='test', payload=data_value)
    time.sleep(5)

