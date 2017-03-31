# -*- coding: utf-8 -*-
import os
import sys, getopt
import paho.mqtt.client as mqtt
import random
import time
import _thread
import socket
import time

HOST = '0.0.0.0'
PORT = 9090
# gb_freq = 0
CONFIG_PATH = 'config/config.cfg'
ITEMS_PATH = 'config/items.cfg'
MILISECOND = 0.001

class Item(object):
    def __init__(self, string):
        self.convert_string_to_item(string)

    def convert_string_to_item(self, string):
        # sensor_name, topic_in,topic_out,frequent
        tokens = str(string).split(',')
        self._platform_type = tokens[0]
        self._sensor_name = tokens[1]
        self._topic = tokens[2]
        self._frequent = int(tokens[3])

    def get_sensor_name(self):
        return self._sensor_name

    def get_topic(self):
        return self._topic

    def get_frequent(self):
        return self._frequent

    def increase_frequent(self):
        self._frequent += 10
        print(self._frequent)
        return self._frequent


class SimulatorEngine(object):
    _bStop = 1

    def __init__(self):
        # read config
        items = [line.rstrip('\n') for line in open(CONFIG_PATH)]
        self._ip_broker = items[0]
        self._port_broker = items[1]
        self._client_name = items[2]
        items = [Item(string=line.rstrip('\n')) for line in open(ITEMS_PATH)]
        self._items = items
        self._mqttc = mqtt.Client(self._client_name)
        self._mqttc.connect(self._ip_broker, int(self._port_broker))

        # hostname = socket.gethostname()

    def send_data(self, item, data=''):
        start_time = time.time()
        time_data_change_period = random.randint(60, 3600)
        time_data_change = time.time()
        data_value = random.randint(0, 100)
        print('Change data value. Period {} Value {}'.format(time_data_change_period, data_value))
        while 1:
            next_time = time.time()
            if next_time - time_data_change >= time_data_change_period:
                time_data_change = next_time
                time_data_change_period = random.randint(60, 3600)
                data_value = random.randint(0, 100)
                print('Change data value. Period {} Value {}'.format(time_data_change_period, data_value))

            if item._platform_type == 'onem2m':
                message = data_value
            else:
                message = '''
                <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <obj>
                    <int val="{value}" name="data"/>
                </obj>
                '''.format(value=data_value)

            self._mqttc.publish(topic=item.get_topic(), payload=message)
            time.sleep(60 / item.get_frequent())
            print('Topic {} -- Data {}'.format(item.get_topic(), data))
            if next_time - start_time >= 3600:
                start_time = next_time
                item.increase_frequent()

    def register_sensor_with_ordinator(self):
        os.system(
            'sensor_detail="$(/bin/hostname -i),$(hostname)" && curl -F "sensor_detail=${sensor_detail}" -F "defined_file=@openhab/demo.items"  ${CO_ORDINATOR_DOMAIN}/sensor/define')

    def execute(self):
        try:
            for item in self._items:
                _thread.start_new_thread(self.send_data, (item,))
        except Exception as e:
            print(e)

        while self._bStop:
            time.sleep(1)


def main(argv):
    engine = SimulatorEngine()
    engine.execute()


if __name__ == '__main__':
    main(sys.argv[1:])

