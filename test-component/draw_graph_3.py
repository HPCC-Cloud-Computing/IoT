import matplotlib.pyplot as plt
import numpy as np
import time
import datetime
import math
from influxdb.influxdb08 import InfluxDBClient

time_min = '2017-03-25 3:10:00'
time_max = '2017-03-25 4:10:00'
time_range = 'time >\'' + time_min + '\' AND time < \'' + time_max + '\' '
time_grouped = '5s'

def query(_field):
    return 'select field, mean(value) from "data_collect_rate" where '+time_range+' AND field=\''+_field+'\' group by time('+time_grouped+'), field fill(0) ;'

def query_metric(_query):
    result = client.query(_query)
    x_val = list()
    y_val = list()
    _time_start = result[0]['points'][0][0]
    for item in result[0]['points']:
        val = 0
        # if len(y_val) > 0:
        #     val = y_val[len(y_val) - 1]
        if item[1]:
            val = item[1]
        # time_stamp = time.mktime(datetime.datetime.strptime(str(item[0]), "%Y-%m-%dT%H:%M:%SZ").timetuple())
        time_stamp = item[0]
        # _time_stp = time_stamp - _time_step
        x_val.append(math.fabs(time_stamp - _time_start) / 5)
        y_val.append(val)
    return {'x': x_val, 'y': y_val}

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'cadvisor')

txt = '''
    Biểu đồ mô tả hoạt động của Post Data Processing.
    Green-line: sensing data input
    Red-line: tần suất đẩy dữ liệu lên cloud
 '''
# color = 'cornflowerblue'
# points = np.ones(2)  # Draw 5 points for each line
# text_style = dict(horizontalalignment='right', verticalalignment='center',
#                   fontsize=12, fontdict={'family': 'monospace'})
# # def format_axes(ax):
# #     ax.margins(0.2)
# #     ax.set_axis_off()
#
#
# def nice_repr(text):
#     return repr(text).lstrip('u')
# fig_2, ax = plt.subplots()
# linestyles = ['-', '--']
# color = ['green', 'red']
# linestylestext = ['data input', 'data output']
# for y, linestyle in enumerate(linestyles):
#     ax.text(-0.1, y, nice_repr(linestyle), **text_style)
#     ax.plot(y * points, linestyle=linestyle, color='cornflowerblue', linewidth=3)
#     # format_axes(ax)
#     ax.set_title('line styles')

data = query_metric(query('in'))
data_2 = query_metric(query('out'))
fig = plt.figure(1)
fig.text(0.5, 0, txt, ha='center')
plt.plot(data['x'], data['y'], 'g', data_2['x'], data_2['y'], 'r',)
plt.ylabel('value')
plt.xlabel('time')
plt.title('Post Data Processing')
plt.grid(True)
plt.show()