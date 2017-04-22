import matplotlib.pyplot as plt
import numpy as np
from influxdb import InfluxDBClient
import time
import datetime
import collections


time_min = '2017-04-03 16:35:00'
time_max = '2017-04-03 22:35:00'
time_min_2 = '2017-04-06 09:30:00'
time_max_2 = '2017-04-06 14:30:00'
# time_min = '2017-03-25 00:00:00'
# time_max = '2017-03-25 11:28:16'

time_grouped = '30s'
time_step = 5
onem2m = ['onem2m-1', 'onem2m-2', 'onem2m-3']
onem2m_naming = {'onem2m-1': '10 messages/m', 'onem2m-2': '20 messages/m', 'onem2m-3': '40 messages/m'}
openhab = ['openhab-1', 'openhab-2', 'openhab-3']
openhab_naming = {'openhab-1': '10 messages/m', 'openhab-2': '20 messages/m', 'openhab-3': '40 messages/m'}
cluster = ['128.199.91.17', '139.59.98.138', '139.59.98.157']
fog_mqtt = ['mqtt']
cloud_mqtt = ['mqtt']
cloud_processing = 'measure-data-rate'
time_range = 'AND time >\'' + time_min + '\' AND time < \'' + time_max + '\' '
fog_namespace = 'kube-system'
cloud_namespace = 'cloud-kube-system'
# sensing_topic = ['onem2m_pf_1/temperature', 'onem2m_pf_6/temperature', 'onem2m_pf_11/temperature',
#                  'openhab_pf_1/temperature', 'openhab_pf_6/temperature', 'openhab_pf_11/temperature']
sensing_topic = ['onem2m_pf_1/temperature','onem2m_pf_6/temperature', 'onem2m_pf_11/temperature', 'openhab_pf_1/temperature', 'openhab_pf_6/temperature', 'openhab_pf_11/temperature']

def cpu_cluster_query(_cluster_name):
    return 'SELECT sum("value")/20 FROM "cpu/usage_rate" WHERE "type" = \'node\' AND "nodename"=\'' + _cluster_name + '\' AND time >\'' + \
           time_min + '\' AND time < \'' + time_max + '\' GROUP BY time(' + str(
        time_grouped) + '), "nodename" fill(null);'

def memory_cluster_query(_cluster_name):
    return 'SELECT sum("value")*100/(1024*1.95) FROM "memory/usage" WHERE "type" = \'node\' ' +time_range+\
           ' AND "nodename"=\''+_cluster_name+'\' ' +\
           'GROUP BY time('+time_grouped+'), "nodename" fill(null);'

def net_cluster_query(_cluster_name):
    return 'SELECT sum("value") FROM "network/tx_rate" WHERE "type" = \'node\' '+\
           time_range + ' AND "nodename"=\''+_cluster_name+'\' ' + \
           ' GROUP BY time('+time_grouped+'), "nodename" fill(null);'

def cpu_query(_pod_name, _namespace):
    return 'SELECT sum("value") FROM "cpu/usage_rate" WHERE "type" = \'pod_container\' AND "namespace_name" = \''+_namespace+'\' AND "pod_name" = \'{pod_name}\' AND time >\''.format(
        pod_name=_pod_name) + \
           time_min + '\' AND time < \'' + time_max + '\' GROUP BY time({time_grouped}), "container_name" fill(null);'.format(
        time_grouped=time_grouped)

def _cpu_query(_namespace):
    return 'SELECT sum("value")/10 FROM "cpu/usage_rate" WHERE "type" = \'pod_container\' AND "namespace_name" = \''+_namespace+'\' AND time >\'' + \
           time_min + '\' AND time < \'' + time_max + '\' GROUP BY time({time_grouped}), "container_name" fill(null);'.format(
        time_grouped=time_grouped)

def _mem_query(_namespace):
    return 'SELECT sum("value")/(1024*1024) FROM "memory/usage" WHERE "type" = \'pod_container\' AND "namespace_name" = \''+_namespace+'\' AND time >\'' + \
           time_min + '\' AND time < \'' + time_max + '\' GROUP BY time({time_grouped}), "container_name" fill(null);'.format(
        time_grouped=time_grouped)

def _mem_query_2(_namespace):
    return 'SELECT * FROM "memory/usage" WHERE "type" = \'pod_container\' AND "namespace_name" = \''+_namespace+'\' AND "container_name"=\'onem2m-1\' AND time =\'' + \
           time_min + '\' ;'.format(
        time_grouped=time_grouped)

def _net_query(_namespace, _group_by):
    return 'SELECT sum("value")/1024 FROM "network/tx_rate" WHERE "type" = \'pod\' AND "namespace_name" = \''+_namespace+'\' AND time >\'' + \
           time_min + '\' AND time < \'' + time_max + '\' GROUP BY time({time_grouped}), "{group_by}" fill(null);'.format(
        time_grouped=time_grouped, group_by=_group_by)

def mem_query(_pod_name, _namespace):
    return 'SELECT sum("value")/(1024*1024) FROM "memory/usage" WHERE "type" = \'pod_container\' AND "namespace_name" = \''+_namespace+'\' AND "pod_name" = \'{pod_name}\' AND time >\''.format(
        pod_name=_pod_name) + \
           time_min + '\' AND time < \'' + time_max + '\' GROUP BY time({time_grouped}), "container_name" fill(null);'.format(
        time_grouped=time_grouped)


def net_query(_pod_name, _namespace):
    return 'SELECT sum("value")/1024 FROM "network/tx_rate" WHERE "type" = \'pod\' AND "namespace_name" = \''+_namespace+'\' AND "pod_name" = \'{pod_name}\' AND time >\''.format(
        pod_name=_pod_name) + \
           time_min + '\' AND time < \'' + time_max + '\' GROUP BY time({time_grouped}) fill(null);'.format(
        time_grouped=time_grouped)


def data_rate_query():
    return 'SELECT sum("num_of_message") FROM "data_collect_rate" WHERE time >\'' + time_min + '\' AND time < \'' + time_max + '\' GROUP BY time({time_grouped});'.format(
        time_grouped=time_grouped)

def data_sensing_query():
    return 'SELECT mean("value") FROM "data_collect_rate" WHERE time >\'' + time_min_2 + '\' AND time < \'' + time_max_2 + '\' GROUP BY time({time_grouped}), "topic_id" fill(null);'.format(
        time_grouped=time_grouped)

def data_deplay_query(select_field):
    return 'SELECT mean("'+select_field+'") FROM "data_collect_rate" WHERE time >\'' + time_min_2 + '\' AND time < \'' + time_max_2 + '\' GROUP BY "num_of_sensor" fill(null);'

# def query_metric(_query):
#     result = client.query(_query)
#     x_val = list()
#     y_val = list()
#     for k, v in result.items():
#         _list = list(v)
#         _time_start = time.mktime(datetime.datetime.strptime(_list[0]['time'], "%Y-%m-%dT%H:%M:%SZ").timetuple())
#         for item in _list:
#             val = 0
#             if len(y_val) > 0:
#                 val = y_val[len(y_val) - 1]
#             if item['sum']:
#                 val = item['sum']
#             time_stamp = time.mktime(datetime.datetime.strptime(item['time'], "%Y-%m-%dT%H:%M:%SZ").timetuple())
#             x_val.append((time_stamp - _time_start) / 60)
#             y_val.append(val)
#         break
#     time.sleep(2)
#     return {'x': x_val, 'y': y_val}

def query_metric(_query, _group_by=None, _aggre_metric=None):
    if (not _group_by) and (not _aggre_metric):
        result = client.query(_query)
        x_val = list()
        y_val = list()
        for k, v in result.items():
            _list = list(v)
            _time_start = time.mktime(datetime.datetime.strptime(_list[0]['time'], "%Y-%m-%dT%H:%M:%SZ").timetuple())
            for item in _list:
                # val = 0
                # if len(y_val) > 0:
                #     val = y_val[len(y_val) - 1]
                val = None
                if item['sum']:
                    val = item['sum']
                time_stamp = time.mktime(datetime.datetime.strptime(item['time'], "%Y-%m-%dT%H:%M:%SZ").timetuple())
                x_val.append((time_stamp - _time_start) / 60)
                y_val.append(val)
            break
        time.sleep(2)
        return {'x': x_val, 'y': y_val}
    result = client.query(_query)
    lines = dict()
    for k, v in result.items():
        _list = list(v)
        _time_start = time.mktime(datetime.datetime.strptime(_list[0]['time'], "%Y-%m-%dT%H:%M:%SZ").timetuple())
        for item in _list:
            # val = 0
            val = None
            if item[_aggre_metric]:
                val = item[_aggre_metric]
            time_stamp = time.mktime(datetime.datetime.strptime(item['time'], "%Y-%m-%dT%H:%M:%SZ").timetuple())
            if not lines.get(k[1][_group_by]):
                lines[k[1][_group_by]] = {'x': list(), 'y': list()}
            lines.get(k[1][_group_by]).get('x').append((time_stamp - _time_start) / 60)
            lines.get(k[1][_group_by]).get('y').append(val)
    time.sleep(2)
    return lines

def mean_values(values, field_1='x', field_2='y'):
    result = []
    result_2 = []
    min_len = len(values[0][field_2])
    if len(values[0][field_1]) > len(values[1][field_1]):
        min_len = len(values[1][field_2])
    if min_len > len(values[2][field_2]):
        min_len = len(values[2][field_2])
    for index in range(0, min_len):
        if values[0][field_2][index] and values[1][field_2][index] and values[2][field_2][index]:
            result.append((values[0][field_2][index] + values[1][field_2][index] + values[2][field_2][index]) / 3)
        else:
            result.append(None)
        result_2.append(values[0][field_1][index])
    return {field_1: result_2, field_2: result}

def gen_plot_by_row(plt, data, y_index,num_col, num_row, row_label, titles, line_type, marker=None, scale=False):
    # num_of_col = len(data)
    x_index = 0
    for item in data:
        if x_index == 0:
            gen_plot(plt=plt, data=item, index=(x_index+y_index*num_col+1), line_type=line_type, y_label=row_label,
                     title=titles[x_index], num_col=num_col, nul_row=num_row, marker=marker, scale=scale)
        else:
            gen_plot(plt=plt, data=item, index=(x_index + y_index * num_col + 1), line_type=line_type,
                     title=titles[x_index], num_col=num_col, nul_row=num_row, marker=marker, scale=scale)
        x_index += 1

def gen_plot(plt, data, index, line_type, num_col, nul_row,y_label=None, x_label='time(s)', title=None, marker=None, scale=False):
    plt.subplot(int('{}{}{}'.format(nul_row, num_col,  index)))
    if isinstance(data, list):
        for line in data:
            plt.plot(line['x'], line['y'])
    elif isinstance(data, dict):
        if data.get('x', 0) == 0:
            count = 0
            temp = dict()
            keys = data.keys()
            sorted(keys)
            for k in keys:
                temp[k] = data[k]
            for _key_group, _values in temp.items():
                series1 = np.array(_values['y']).astype(np.double)
                s1mask = np.isfinite(series1)
                series = np.array(_values['x'])
                if len(data) > 3:
                    # plt.plot(series[s1mask], series1[s1mask], marker=marker[count], linewidth=1)
                    plt.plot(series[s1mask], series1[s1mask], linewidth=2, linestyle = line_type[count])
                else:
                    plt.plot(series[s1mask], series1[s1mask], linewidth=1)
                if scale:
                    plt.yscale('log')
                count += 1
                # plt.plot(_values['x'], _values['y'])
            # plt.legend(data.keys(), ncol=int(len(data.keys())/3), loc='upper left')
            plt.legend(data.keys(), ncol=int(len(data.keys())/3), loc='upper right', columnspacing=1.5, labelspacing=0.0,
           handletextpad=0.0, handlelength=1.0, fontsize='small')
        else:
            plt.plot(data['x'], data['y'], line_type[0])
    if y_label:
        plt.ylabel(y_label)
    if x_label:
        plt.xlabel(x_label)
    plt.title(title)
    plt.grid(True)
    plt.xticks(np.arange(0, 360 + 1, 30.0))
    # plt.xticks(np.arange(0, 120 + 1, 10.0))

def draw_graps(data=dict()):
    line_type = ['-', '-.', '--', ':', '-.', '--']
    marker = ['.', 'o', 'v', 'x', '+', '<', '*']
    # plot with various axes scales
    plt.figure(1)
    # cpu
    # col_1 = {onem2m_naming[k]: data['fog']['cpu'][k] for k in onem2m}
    # # col_1['mean'] = mean_values(list(col_1.values()))
    # col_2 = {openhab_naming[k]: data['fog']['cpu'][k] for k in openhab}
    # # col_2['mean'] = mean_values(list(col_2.values()))
    # col_3 = {k: data['fog']['cpu'][k] for k in fog_mqtt}
    # rows = [col_1, col_2, col_3]
    # titles = ['ONEM2M CPU USAGE', 'OPENHAB CPU USAGE', 'MQTT CPU USAGE']
    # gen_plot_by_row(plt=plt, data=rows, y_index=0, row_label='cpu_usage(%)', titles=titles,  num_col=len(data['fog']), num_row=3,
    #                 line_type=line_type)
    #
    # col_1 = {onem2m_naming[k]: data['fog']['memory'][k] for k in onem2m}
    # # col_1['mean'] = mean_values(list(col_1.values()))
    # col_2 = {openhab_naming[k]: data['fog']['memory'][k] for k in openhab}
    # # col_2['mean'] = mean_values(list(col_2.values()))
    # col_3 = {k: data['fog']['memory'][k] for k in fog_mqtt}
    # rows = [col_1, col_2, col_3]
    # titles = ['ONEM2M MEM USAGE', 'OPENHAB MEM USAGE', 'MQTT MEM USAGE']
    # gen_plot_by_row(plt=plt, data=rows, y_index=1, row_label='memory_usage(MB)', titles=titles, num_col=len(data['fog']), num_row=3,
    #                 line_type=line_type)
    #
    # col_1 = {onem2m_naming[k]: data['fog']['network'].get('app:{}'.format(k)) for k in onem2m}
    # # col_1['mean'] = mean_values(list(col_1.values()))
    # col_2 = {openhab_naming[k]: data['fog']['network'].get('app:{}'.format(k)) for k in openhab}
    # # col_2['mean'] = mean_values(list(col_2.values()))
    # col_3 = {k: data['fog']['network'].get('app:{}'.format(k)) for k in fog_mqtt}
    # rows = [col_1, col_2, col_3]
    # titles = ['ONEM2M NET USAGE', 'OPENHAB NET USAGE', 'MQTT NET USAGE']
    # gen_plot_by_row(plt=plt, data=rows, y_index=2, row_label='network_usage(kBps)', titles=titles, num_col=len(data['fog']), num_row=3,
    #                 line_type=line_type)
    # plt.subplots_adjust(top=0.93, bottom=0.07, left=0.05, right=0.96, hspace=0.51,
    #                     wspace=0.19)
    # plt.show()
    # #
    # # ################
    # plt.figure(2)
    # col_1 = {cloud_processing: data['cloud']['cpu'][cloud_processing]}
    # # col_2 = {cloud_mqtt: data['cloud']['cpu'][cloud_mqtt]}
    # col_2 = {k: data['cloud']['cpu'][k] for k in cloud_mqtt}
    # rows = [col_1, col_2]
    # titles = ['DATA_PROCESSING CPU USAGE', 'CLOUD MQTT CPU USAGE']
    # gen_plot_by_row(plt=plt, data=rows, y_index=0, row_label='cpu_usage(%)', titles=titles, num_col=2, num_row=3,
    #                 line_type=line_type)
    #
    # col_1 = {cloud_processing: data['cloud']['memory'][cloud_processing]}
    # # col_2 = {cloud_mqtt: data['cloud']['memory'][cloud_mqtt]}
    # col_2 = {k: data['cloud']['memory'][k] for k in cloud_mqtt}
    # rows = [col_1, col_2]
    # # rows = [data['cloud']['memory'][cloud_processing], data['cloud']['memory'][cloud_mqtt]]
    # titles = ['DATA_PROCESSING MEM USAGE', 'CLOUD MQTT MEM USAGE']
    # gen_plot_by_row(plt=plt, data=rows, y_index=1, row_label='memory_usage(MB)', titles=titles, num_col=2, num_row=3,
    #                 line_type=line_type)
    #
    # col_1 = {cloud_processing: data['cloud']['network'][cloud_processing]}
    # # col_2 = {cloud_mqtt: data['cloud']['network'][cloud_mqtt]}
    # col_2 = {k: data['cloud']['network'][k] for k in cloud_mqtt}
    # rows = [col_1, col_2]
    # # rows = [data['cloud']['network'][cloud_processing], data['cloud']['network'][cloud_mqtt]]
    # titles = ['DATA_PROCESSING NET USAGE', 'CLOUD MQTT NET USAGE']
    # gen_plot_by_row(plt=plt, data=rows, y_index=2, row_label='network_usage(kBps)', titles=titles, num_col=2, num_row=3,
    #                 line_type=line_type)
    # plt.show()

    #################
    plt.figure(3)

    rows = [{k: data['cloud']['sensing_data'][k] for k in sensing_topic}]
    titles = ['SENSING DATA']
    gen_plot_by_row(plt=plt, data=rows, y_index=0, row_label='Value', titles=titles, num_col=1,
                    num_row=1,
                    line_type=line_type, marker=marker)

    # show
    plt.subplots_adjust(top=0.93, bottom=0.07, left=0.05, right=0.99, hspace=0.85,
                        wspace=0.19)
    plt.show()
    return


client = InfluxDBClient('188.166.238.158', 32485, 'root', 'root', 'k8s')
data = dict()

# get metric
pod_names = {'fog': {'onem2m': onem2m, 'openhab': openhab, 'mqtt': fog_mqtt}, 'cloud': {'mqtt': cloud_mqtt, 'processing': cloud_processing}}
namespaces = {'fog': fog_namespace, 'cloud': cloud_namespace}
resource_metrics = {'cpu', 'memory', 'network'}
resource_query = {'cpu': _cpu_query, 'memory': _mem_query, 'network': _net_query}
data['fog'] = dict()
data['cloud'] = dict()
# data['fog']['cpu'] = query_metric(_cpu_query(namespaces['fog']), 'container_name', 'sum')
# data['fog']['memory'] = query_metric(_mem_query(namespaces['fog']), 'container_name', 'sum')
# data['fog']['network'] = query_metric(_net_query(namespaces['fog'], 'labels'), 'labels', 'sum')
# temp = dict(data['fog']['network'])
# for key, value in temp.items():
#     for check_key in onem2m:
#         if key.find(check_key) >= 0:
#             data['fog']['network'][check_key] = value
#             continue
#     for check_key in openhab:
#         if key.find(check_key) >= 0:
#             data['fog']['network'][check_key] = value
#             continue
#     for check_key in fog_mqtt:
#         if key.find(check_key) >= 0:
#             data['fog']['network'][check_key] = value
#             continue
#
# print('query fog done')
# data['cloud']['cpu'] = query_metric(_cpu_query(namespaces['cloud']), 'container_name', 'sum')
# data['cloud']['memory'] = query_metric(_mem_query(namespaces['cloud']), 'container_name', 'sum')
# data['cloud']['network'] = query_metric(_net_query(namespaces['cloud'], 'pod_name'), 'pod_name', 'sum')
# temp = dict(data['cloud']['network'])
# for key, value in temp.items():
#     for check_key in cloud_mqtt:
#         if key.find(check_key) >= 0:
#             data['cloud']['network'][check_key] = value
#             continue
#     if key.find(cloud_processing) >= 0:
#         data['cloud']['network'][cloud_processing] = value
#         continue
# data['cloud']['sensing_data'] = query_metric(data_sensing_query(), 'topic_id', 'mean')
# for k,v in data['cloud']['sensing_data'].items():
#     print(k)
#     print(v)
print('query cloud done')
# draw_graps(data)

# _data = client.query(data_deplay_query('round_trip_3'))
# for k, v in _data.items():
#     print(k[1]['num_of_sensor'])
#     print(list(v)[0]['mean'])
# print('-----------------------------------------------')

# _data_1 = client.query(data_deplay_query('time_send_cloud'))
# series_1 = {'x': list(), 'y': list()}
# for k, v in _data_1.items():
#     # series_1['x'].append(int(k[1]['num_of_sensor']))
#     # series_1['y'].append(float(list(v)[0]['mean']))
#     print(k[1]['num_of_sensor'])
#     print(list(v)[0])
    # print(list(v)[0]['mean'])
#
_data_1 = client.query(data_deplay_query('round_trip_1'))
series_1 = {'x': list(), 'y': list()}
for k, v in _data_1.items():
    series_1['x'].append(int(k[1]['num_of_sensor']))
    series_1['y'].append(float(list(v)[0]['mean']))
    # print(k[1]['num_of_sensor'])
    # print(list(v)[0]['mean'])
print('-----------------------------------------------')
series_2 = {'x': list(), 'y': list()}
_data_2 = client.query(data_deplay_query('round_trip_2'))

for k, v in _data_2.items():
    # print(k[1]['num_of_sensor'])
    # print(list(v)[0]['mean'])
    series_2['x'].append(int(k[1]['num_of_sensor']))
    series_2['y'].append(float(list(v)[0]['mean']+1))

print(series_1)
print(series_2)

width = 1       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(series_1['x'], series_1['y'], width, color='#d62728')
p2 = plt.bar(series_2['x'], series_2['y'], width,
             bottom=series_1['y'])


plt.ylabel('Transmission Time (seconds)')
plt.xlabel('Number of sensors per platform (on 5 platforms)')
plt.title('Tranmission time by number of sensor')
plt.xticks(series_1['x'])
# plt.yticks(np.arange(0, 300, 10))
plt.legend((p1[0], p2[0]), ('Sensor - Platform Transmission Time', 'Platform - Cloud Transmission Time'))

# def autolabel(rects):
#     """
#     Attach a text label above each bar displaying its height
#     """
#     for rect in rects:
#         height = rect.get_height()
#         plt.text(rect.get_x() + rect.get_width()/2., 1.05*height,
#                 '%d' % int(height),
#                 ha='center', va='bottom')

plt.show()
