from influxdb import InfluxDBClient
client = InfluxDBClient('188.166.238.158', 32485, 'root', 'root', 'k8s')
import time
time_min = '2017-02-27 18:30:00'
time_max = '2017-02-27 20:30:00'
# query = 'SELECT min("value") FROM "cpu/usage_rate" WHERE "type" = \'pod_container\' AND "namespace_name" = \'kube-system\' AND "pod_name" = \'openhab-m606f\' AND time >\''+time_min+'\' AND time < \''+time_max+'\' GROUP BY "container_name" fill(null);'
query = 'SELECT sum("value") FROM "cpu/usage_rate" WHERE "type" = \'pod_container\' AND "namespace_name" = \'kube-system\' AND "pod_name" = \'openhab-m606f\' AND time >\''+time_min+'\' AND time < \''+time_max+'\' GROUP BY time(2m), "container_name" fill(null);'
# query = 'SELECT sum("value") FROM "cpu/usage_rate" WHERE "type" = \'pod_container\' AND "namespace_name" = \'kube-system\' AND "pod_name" = \'openhab-m606f\' AND time =\''+time_min+'\' GROUP BY time(2m), "container_name" fill(null);'
result = client.query(query)
for k,v in result.items():
  _list = list(v)
  sum = 0
  n = 0
  for item in _list:
  	if item['sum']:
  		print(item)
  	# if item['sum']:
  	# 	sum += item['sum']
  	# 	n += 1
  # print(sum/n)

