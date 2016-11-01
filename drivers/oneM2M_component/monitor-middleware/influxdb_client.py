import os

__author__ = 'huanpc'

from influxdb import InfluxDBClient
import xml.etree.ElementTree as ET


def store_data(xml_data=None):
    root = ET.fromstring(xml_data)
    ipe_id = root.find('./*[@name="ipeId"]').attrib['val']
    app_id = root.find('./*[@name="appId"]').attrib['val']
    category = root.find('./*[@name="category"]').attrib['val']
    data = int(root.find('./*[@name="data"]').attrib['val'])
    unit = root.find('./*[@name="unit"]').attrib['val']
    json_body = [
        {
            "measurement": "sensor_status",
            "tags": {
                "sensor_id": app_id,
                "ipe_id": ipe_id,
                "category": category
            },
            "fields": {
                "data": data,
                "unit": unit
            }
        }
    ]
    influxdb_host = 'localhost'
    if os.environ.get('INFLUXDB_HOST_NAME'):
        influxdb_host = os.environ['INFLUXDB_HOST_NAME']
    client = InfluxDBClient(influxdb_host, os.environ.get('INFLUXDB_PORT'), 'root', 'root', 'oneM2M')
    client.write_points(json_body)
    # result = client.query('select * from sensor_status;')
    # print("Result: {0}".format(result))

# if __name__ == '__main__':
#     xml_data = '''
#     <obj>
#         <str val="demo" name="ipeId"/>
#         <str val="TEMPERATURE_SENSOR" name="appId"/>
#         <str val="temperature" name="category"/>
#         <int val="77" name="data"/>
#         <str val="celsius" name="unit"/>
#     </obj>
#     '''
#     store_data(xml_data)
