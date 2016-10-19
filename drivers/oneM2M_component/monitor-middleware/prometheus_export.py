__author__ = 'huanpc'

from prometheus_client import start_http_server, Summary, Gauge
import random
import time

from influxdb import InfluxDBClient
import xml.etree.ElementTree as ET



# def f(i=None):
#   g.set(i)
#   pass
#
# # with gd():
# #   i+=1
# #   g.set(i)
# #   pass
#
# # Decorate function with metric.
# @REQUEST_TIME.time()
# def process_request(t):
#     """A dummy function that takes some time."""
#     time.sleep(t)
#
# if __name__ == '__main__':
#     # Start up the server to expose the metrics.
#     start_http_server(8001)
#
#     # Generate some requests.
#     while True:
#         i+=1
#         f(i)
#         process_request(random.random())

def export_data(xml_data=None):
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

class PrometheusClient:

    def __init__(self):
        #     # Start up the server to expose the metrics.
        start_http_server(8001)
        self.g = Gauge('sensor_data', 'Value gathered by sensor', ['sensor_id', 'ipe_id', 'category_id', 'unit'])

    def export_data(self, xml_data=None):
        root = ET.fromstring(xml_data)
        ipe_id = root.find('./*[@name="ipeId"]').attrib['val']
        app_id = root.find('./*[@name="appId"]').attrib['val']
        category = root.find('./*[@name="category"]').attrib['val']
        data = int(root.find('./*[@name="data"]').attrib['val'])
        unit = root.find('./*[@name="unit"]').attrib['val']
        # json_body = [
        #     {
        #         "measurement": "sensor_status",
        #         "tags": {
        #             "sensor_id": app_id,
        #             "ipe_id": ipe_id,
        #             "category": category
        #         },
        #         "fields": {
        #             "data": data,
        #             "unit": unit
        #         }
        #     }
        # ]
        self.g.labels(app_id, ipe_id, category, unit).set(data)


