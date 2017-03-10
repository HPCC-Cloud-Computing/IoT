# -*- coding: utf-8 -*-
import os

import paho.mqtt.client as mqtt
import random
import time
import _thread
import socket
import time
HOST = '0.0.0.0'
PORT = 9090
parent_path = ''
gb_freq = 0


def read_config():
    global ip_broker
    global port_broker
    global topic_in
    global topic_out
    global hostname
    f = open(parent_path + 'config/config.cfg', 'r')
    ip_broker = f.readline().replace('\n', '')
    port_broker = f.readline().replace('\n', '')
    # hostname = socket.gethostname()
    hostname = 'sdfd'
    # topic_in = hostname + '_' + f.readline().replace('\n', '')
    # topic_out = hostname + '_' + f.readline().replace('\n', '')
    topic_in = f.readline().replace('\n', '')
    topic_out = f.readline().replace('\n', '')
    global number_sensor
    # number_sensor = int(f.readline().replace('\n', ''))
    number_sensor = 10
    global gb_freq
    # freq = int(f.readline().replace('\n', ''))
    gb_freq = 40
    f.close()


# Number    MyTemperature  "Temperature [%.1f °C]"         {mqtt="<[mos:/temp:state:default], >[mos:/out:state:*:default]"}
def write_item_file():
    try:
        f = open(parent_path + 'openhab/demo.items', 'w')
        for i in range(0, number_sensor):
            f.write('Number {}_sensor_{}'.format(hostname, str(i)) + ' "Value [%.1f]" {mqtt="<[mqttIn:' + topic_in + str(
                i) + ':state:default], >[mqttOut:' + topic_out + str(i) + ':state:*:default]"}' + '\n')
    except IOError:
        print('Can not open file item\n')
    else:
        f.close()


# sitemap demo label="Demo House"
# {
# 	Text item=MyTemperature
# }
def write_sitemap_file():
    try:
        f = open(parent_path + 'openhab/demo.sitemap', 'w')
        f.write('sitemap demo label="Demo House"\n{' + '\n')
        for i in range(0, number_sensor):
            f.write('Text item={}_sensor_{}'.format(hostname, str(i)) + '\n')
        f.writelines('}')
    except IOError:
        print('Can not open file sitemap\n')
    else:
        f.close()


def send_data(di):
    global gb_freq
    start_time = time.time()
    while 1:
        mqttc.publish("onem2m/humidity", random.randint(-10, 100))
        # mqttc.publish('/in' + str(di), random.randint(-10, 100))
        # mqttc.publish('/in' + str(di), 'sdff')
        time.sleep(60/gb_freq)
        print('{} -- Running'.format(topic_in+ str(di)))
        next_time = time.time()
        if next_time - start_time >= 3600:
            start_time = next_time
            change_sensor_freq()

def change_sensor_freq():
    global gb_freq
    gb_freq += 10

def change_sensor_quantity():
    pass

def register_sensor_with_ordinator():
    os.system(
        'sensor_detail="$(/bin/hostname -i),$(hostname)" && curl -F "sensor_detail=${sensor_detail}" -F "defined_file=@openhab/demo.items"  ${CO_ORDINATOR_DOMAIN}/sensor/define')


MILISECOND = 0.001
read_config()
mqttc = mqtt.Client('python_pub')
mqttc.connect(ip_broker, int(port_broker))
bStop = 1
write_item_file()
write_sitemap_file()
# co_ordinator_host = os.environ.get('CO_ORDINATOR_DOMAIN')
# register_sensor_with_ordinator()

# @asyncio.coroutine
# def get_sensor_description(request):
#     lines = [line.rstrip('\n') for line in open(parent_path + 'openhab/demo.items')]
#     content = '\n'.join(lines)
#     return web.Response(status=200, body=content.encode('utf-8'))
#
# @asyncio.coroutine
# def init(loop):
#     app = web.Application(loop=loop)
#     # Get resource description
#     app.router.add_route('GET', '/sensor/description', get_sensor_description)
#
#     srv = yield from loop.create_server(app.make_handler(), HOST, PORT)
#     print("Server started at " + HOST + ":" + str(PORT))
#     return srv
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(init(loop))

try:

    for i in range(0, number_sensor):
        _thread.start_new_thread(send_data, (i,))
except Exception as e:
    print('Can not create thread\n')
#
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass

while bStop:
    time.sleep(1)
