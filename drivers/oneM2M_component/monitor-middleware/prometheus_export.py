__author__ = 'huanpc'

from prometheus_client import start_http_server, Summary, Gauge
import random
import time

from influxdb import InfluxDBClient
import xml.etree.ElementTree as ET

EXPORT_PORT = '8001'


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
        start_http_server(EXPORT_PORT)
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
