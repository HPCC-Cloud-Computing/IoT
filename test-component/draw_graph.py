import matplotlib.pyplot as plt
import numpy as np
from influxdb import InfluxDBClient
client = InfluxDBClient('188.166.238.158', 32485, 'root', 'root', 'k8s')
import time
import datetime
time_min = '2017-03-03 11:00:00'
time_max = '2017-03-03 17:00:00'
time_grouped = '1m'
time_step = 5
onem2m = 'openhab-dtvsr'
sensor_pod_name = 'sensor-gen-st0pn'

def cpu_query(_pod_name):
    return 'SELECT sum("value")/10 FROM "cpu/usage_rate" WHERE "type" = \'pod_container\' AND "namespace_name" = \'kube-system\' AND "pod_name" = \'{pod_name}\' AND time >\''.format(
        pod_name=_pod_name) + \
                time_min + '\' AND time < \'' + time_max + '\' GROUP BY time({time_grouped}), "container_name" fill(null);'.format(time_grouped=time_grouped)

def mem_query(_pod_name):
    return 'SELECT sum("value")/(1024*1024) FROM "memory/usage" WHERE "type" = \'pod_container\' AND "namespace_name" = \'kube-system\' AND "pod_name" = \'{pod_name}\' AND time >\''.format(
        pod_name=_pod_name) + \
    time_min + '\' AND time < \'' + time_max + '\' GROUP BY time({time_grouped}), "container_name" fill(null);'.format(time_grouped=time_grouped)

def net_query(_pod_name):
    return 'SELECT sum("value")/1024 FROM "network/tx_rate" WHERE "type" = \'pod\' AND "namespace_name" = \'kube-system\' AND "pod_name" = \'{pod_name}\' AND time >\''.format(
        pod_name=_pod_name) + \
    time_min + '\' AND time < \'' + time_max + '\' GROUP BY time({time_grouped}) fill(null);'.format(time_grouped=time_grouped)

def data_rate_query():
    return 'SELECT sum("num_of_message") FROM "data_collect_rate" WHERE time >\''+time_min+'\' AND time < \''+time_max+'\' GROUP BY time({time_grouped});'.format(time_grouped=time_grouped)

def query_metric(_query):
    result = client.query(_query)
    x_val = list()
    y_val = list()
    for k, v in result.items():
        _list = list(v)
        _time_step = 0
        _time_start = time.mktime(datetime.datetime.strptime(_list[0]['time'], "%Y-%m-%dT%H:%M:%SZ").timetuple())
        for item in _list:
            # print(item)
            if item['sum']:
                time_stamp = time.mktime(datetime.datetime.strptime(item['time'], "%Y-%m-%dT%H:%M:%SZ").timetuple())
                # _time_stp = time_stamp - _time_step
                x_val.append((time_stamp-_time_start)/60)
                y_val.append(item['sum'])
                # _time_step = time_stamp
                # _time_step += time_step
        break
    return {'x': x_val, 'y': y_val}

def draw_graps(data=dict()):
    # plot with various axes scales
    plt.figure(1)
    # cpu
    #
    plt.subplot(421)
    plt.plot(data['platform']['cpu']['x'], data['platform']['cpu']['y'])
    plt.ylabel('cpu_usage(%)')
    plt.xlabel('time')
    plt.title('PF CPU USAGE')
    plt.grid(True)
    plt.xticks(np.arange(0, 360 + 1, 30.0))
    #
    plt.subplot(422)
    plt.plot(data['sensor']['cpu']['x'], data['sensor']['cpu']['y'], 'r')
    plt.ylabel('cpu_usage(%)')
    plt.xlabel('time(s)')
    plt.title('SEN CPU USAGE')
    plt.grid(True)
    plt.xticks(np.arange(0, 360 + 1, 30.0))
    # memory
    #
    plt.subplot(423)
    plt.plot(data['platform']['memory']['x'], data['platform']['memory']['y'])
    plt.ylabel('memory_usage(MB)')
    plt.xlabel('time')
    plt.title('PF MEM USAGE')
    plt.grid(True)
    plt.xticks(np.arange(0, 360 + 1, 30.0))
    #
    plt.subplot(424)
    plt.plot(data['sensor']['memory']['x'], data['sensor']['memory']['y'], 'r')
    plt.ylabel('memory_usage(MB)')
    plt.xlabel('time(s)')
    plt.title('SEN MEM USAGE')
    plt.grid(True)
    plt.xticks(np.arange(0, 360 + 1, 30.0))
    # network
    #
    plt.subplot(425)
    plt.plot(data['platform']['network']['x'], data['platform']['network']['y'])
    plt.ylabel('network_usage(kBps)')
    plt.xlabel('time(s)')
    plt.title('PF NET USAGE')
    plt.grid(True)
    # plt.subplots_adjust(top=0.92, bottom=0.11, left=0.13, right=0.95, hspace=0.9,
    #                     wspace=0.2)
    plt.xticks(np.arange(0, 360 + 1, 30.0))
    #
    plt.subplot(426)
    plt.plot(data['sensor']['network']['x'], data['sensor']['network']['y'], 'r')
    plt.ylabel('network_usage(kBps)')
    plt.xlabel('time(s)')
    plt.title('SEN NET USAGE')
    plt.grid(True)
    # plt.subplots_adjust(top=0.92, bottom=0.11, left=0.13, right=0.95, hspace=0.9,
    #                     wspace=0.2)
    plt.xticks(np.arange(0, 360 + 1, 30.0))
    # data rate
    plt.subplot(427)
    plt.plot(data['data_rate']['x'], data['data_rate']['y'], 'g')
    plt.ylabel('messages/sec')
    plt.xlabel('time(s)')
    plt.title('DATA RATE')
    plt.grid(True)
    plt.subplots_adjust(top=0.92, bottom=0.06, left=0.13, right=0.95, hspace=0.9,
                        wspace=0.3)
    plt.xticks(np.arange(0, 360 + 1, 30.0))

    # show
    plt.show()
    return

data = dict()
# get cpu metric
data['platform'] = dict()
data['sensor'] = dict()
data['platform']['cpu'] = query_metric(_query=cpu_query(onem2m))
data['sensor']['cpu'] = query_metric(_query=cpu_query(sensor_pod_name))
# print(data['cpu'])
# # get memory metric
data['platform']['memory'] = query_metric(_query=mem_query(onem2m))
data['sensor']['memory'] = query_metric(_query=mem_query(sensor_pod_name))
# get network metric
data['platform']['network'] = query_metric(_query=net_query(onem2m))
data['sensor']['network'] = query_metric(_query=net_query(sensor_pod_name))
# get data rate
data['data_rate'] = query_metric(_query=data_rate_query())
# draw graph
draw_graps(data)