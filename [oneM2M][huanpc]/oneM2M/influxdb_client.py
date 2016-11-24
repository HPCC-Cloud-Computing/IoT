__author__ = 'huanpc'

from influxdb import InfluxDBClient
import xml.etree.ElementTree as ET

def store_data(xml_data=None):
    root = ET.fromstring(xml_data)
    app_id = root.find('./*[@name="appId"]').attrib['val']
    category = root.find('./*[@name="category"]').attrib['val']
    data = int(root.find('./*[@name="data"]').attrib['val'])
    unit = root.find('./*[@name="unit"]').attrib['val']
    json_body = [
        {
            "measurement": "sensor_status",
            "tags": {
                "sensor_id": app_id,
                "category": category
            },
            "fields": {
                "data": data,
                "unit": unit
            }
        }
    ]
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'oneM2M')
    client.write_points(json_body)
    # result = client.query('select * from sensor_status;')
    # print("Result: {0}".format(result))

# if __name__ == '__main__':
#     xml_data = '''
#     <obj>
#         <str val="TEMPERATURE_SENSOR" name="appId"/>
#         <str val="temperature" name="category"/>
#         <int val="77" name="data"/>
#         <str val="celsius" name="unit"/>
#     </obj>
#     '''
#     store_data(xml_data)
