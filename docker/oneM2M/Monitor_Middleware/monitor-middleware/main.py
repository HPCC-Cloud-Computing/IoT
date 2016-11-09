#! /usr/bin/python3

__author__ = 'huanpc'

import asyncio

import http.client

from aiohttp import web

import logging

import sys

import cloudAMPQclient

import influxdb_client
from prometheus_export import PrometheusClient
import os

PROTOCOL = 'http'
HOST = '0.0.0.0'
PORT = 9090
M2M_HOST = '127.0.0.1'
if os.environ.get('ONEM2M_HOST_NAME'):
    M2M_HOST = os.environ['ONEM2M_HOST_NAME']
M2M_PORT = '8080'
if os.environ.get('ONEM2M_PORT'):
    M2M_PORT = os.environ['ONEM2M_PORT']
DOMAIN = M2M_HOST + ':' + M2M_PORT
HOST_NAME = HOST
if os.environ.get('HOST_NAME'):
    HOST_NAME = os.environ['HOST_NAME']

logger = logging.getLogger('RESOURCE_TRACKING')
logging.basicConfig(stream=sys.stderr, level=getattr(logging, 'INFO'))
prometheus_client = PrometheusClient()


@asyncio.coroutine
def get_resource_state(request):
    app_id = request.match_info.get('app_id')
    if app_id == 'all':
        app_ids = ['TEMPERATURE_SENSOR', 'AIR_HUMIDITY_SENSOR', 'LIGHT_SENSOR']
        all_response = '<?xml version="1.0" encoding="UTF-8"?><root>'
        for app_id in app_ids:
            resource_uri = '/~/' + 'mn-cse/mn-name' + '/' + app_id + '/' + 'DATA' + '/' + 'la'
            con = http.client.HTTPConnection(DOMAIN)
            header = {'X-M2M-Origin': 'admin:admin', "Content-type": "application/xml"}
            con.request('GET', resource_uri, '', header)
            response = con.getresponse()
            raw = response.read().decode()
            raw = raw.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
            all_response += raw
        all_response += '</root>'
        logger.info("Request: GET/URI:" + all_response)
        return web.Response(status=200, body=all_response.encode('utf-8'), content_type="application/xml")
    else:
        # 'http://127.0.0.1:8080/~/mn-cse/mn-name/LAMP_0/DATA/la'
        resource_uri = '/~/' + 'mn-cse/mn-name' + '/' + app_id + '/' + 'DATA' + '/' + 'la'
        con = http.client.HTTPConnection(DOMAIN)
        header = {'X-M2M-Origin': 'admin:admin', "Content-type": "application/xml"}
        con.request('GET', resource_uri, '', header)
        response = con.getresponse()
        logger.info("Request: GET/URI:" + resource_uri)
        return web.Response(status=200, body=response.read(), content_type="application/xml")


@asyncio.coroutine
def get_all_resources_uri(request):
    # http://127.0.0.1:8080/~/mn-cse?fu=1&poa=sample&ty=2
    uri = '/~/mn-cse?fu=1&poa=sample&ty=2'
    con = http.client.HTTPConnection(DOMAIN)
    header = {'X-M2M-Origin': 'admin:admin', "Content-type": "application/xml"}
    con.request('GET', uri, '', header)
    response = con.getresponse()
    logger.info("Request: GET/URI:" + uri)
    return web.Response(status=200, body=response.read().decode().encode('utf-8'))


@asyncio.coroutine
def get_all_resources_descriptor(request):
    # http://127.0.0.1:8080/~/mn-cse/mn-name/TEMPERATURE_SENSOR/DESCRIPTOR/la
    uri = '/~/mn-cse/mn-name/TEMPERATURE_SENSOR/DESCRIPTOR/la'
    con = http.client.HTTPConnection(DOMAIN)
    header = {'X-M2M-Origin': 'admin:admin', "Content-type": "application/xml"}
    con.request('GET', uri, '', header)
    response = con.getresponse()
    logger.info("Request: GET/URI:" + uri)
    return web.Response(status=200, body=response.read().decode().encode('utf-8'))


@asyncio.coroutine
def get_all_resource_state():
    app_ids = ['TEMPERATURE_SENSOR', 'AIR_HUMIDITY_SENSOR', 'LIGHT_SENSOR']
    # 'http://127.0.0.1:8080/~/mn-cse/mn-name/LAMP_0/DATA/la'
    all_response = '<root>'
    for app_id in app_ids:
        resource_uri = '/~/' + 'mn-cse/mn-name' + '/' + app_id + '/' + 'DATA' + '/' + 'la'
        con = http.client.HTTPConnection(DOMAIN)
        header = {'X-M2M-Origin': 'admin:admin', "Content-type": "application/xml"}
        con.request('GET', resource_uri, '', header)
        response = con.getresponse()
        all_response += response.read().decode()
    all_response += '</root>'
    logger.info("Request: GET/URI:" + all_response)
    return web.Response(status=200, body=all_response.encode('utf-8'))


@asyncio.coroutine
def monitor_all_register(request):
    one_m2m_host = request.match_info.get('oneM2M_host')
    one_m2m_uri = one_m2m_host+':'+M2M_PORT
    api = 'sample'
    logger.info("DOMAIN: " + DOMAIN)
    logger.info("monitor_all: " + api)
    for resource_id in get_all_resource_id(api=api, one_m2m_uri=one_m2m_uri):
        monitor_register_one(resource_id, one_m2m_uri=one_m2m_uri)
    return web.Response(status=200, body=' '.encode('utf-8'))


def get_all_resource_id(api, one_m2m_uri):
    # http://127.0.0.1:8080/~/mn-cse/mn-name?fu=1&api=sample&ty=2
    # <m2m:uril xmlns:m2m="http://www.onem2m.org/xml/protocols">/mn-cse/mn-name/AIR_HUMIDITY_SENSOR_1 /mn-cse/mn-name/AIR_HUMIDITY_SENSOR_2 /mn-cse/mn-name/AIR_HUMIDITY_SENSOR_3 /mn-cse/mn-name/AIR_HUMIDITY_SENSOR_4 /mn-cse/mn-name/AIR_HUMIDITY_SENSOR_5 /mn-cse/mn-name/HUMAN_APPEARANCE /mn-cse/mn-name/TEMPERATURE_SENSOR_1 /mn-cse/mn-name/TEMPERATURE_SENSOR_2 /mn-cse/mn-name/TEMPERATURE_SENSOR_3 /mn-cse/mn-name/TEMPERATURE_SENSOR_4 /mn-cse/mn-name/TEMPERATURE_SENSOR_5</m2m:uril>
    resource_uri = '/~/in-cse/in-name?fu=1&api={}&ty=2'.format(api)
    con = http.client.HTTPConnection(one_m2m_uri)
    header = {'X-M2M-Origin': 'admin:admin'}
    con.request('GET', resource_uri, None, header)
    response = con.getresponse().read().decode()
    string_start = '<m2m:uril xmlns:m2m="http://www.onem2m.org/xml/protocols">'
    response = response[response.find(string_start) + len(string_start):response.find('</m2m:uril>')]
    list_uri = response.split(' ')
    return list_uri


def monitor_register_one(resource_uri, one_m2m_uri):
    resource_uri = '/~' + resource_uri + '/DATA'
    con = http.client.HTTPConnection(one_m2m_uri)
    header = {'X-M2M-Origin': 'admin:admin', "Content-type": "application/xml;ty=23", "X-M2M-NM": "SUB_MY_SENSOR",
              "Connection": "close"}
    body = """
        <m2m:sub xmlns:m2m="http://www.onem2m.org/xml/protocols">
            <nu>http://{host}:{port}/monitor</nu>
            <nct>2</nct>
        </m2m:sub>
    """.format(host=HOST_NAME, port=PORT)
    con.request('POST', resource_uri, body.encode('utf-8'), header)
    # response = con.getresponse()
    logger.info("Monitor: " + resource_uri)


@asyncio.coroutine
def monitor_register(request):
    app_id = request.match_info.get('app_id')
    resource_uri = '/~/' + 'mn-cse/mn-name' + '/' + app_id + '/' + 'DATA'
    con = http.client.HTTPConnection(DOMAIN)
    header = {'X-M2M-Origin': 'admin:admin', "Content-type": "application/xml;ty=23", "X-M2M-NM": "SUB_MY_SENSOR_2",
              "Connection": "close"}
    body = """
        <m2m:sub xmlns:m2m="http://www.onem2m.org/xml/protocols">
            <nu>http://{host}:{port}/monitor</nu>
            <nct>2</nct>
        </m2m:sub>
    """.format(host=HOST, port=PORT)
    con.request('POST', resource_uri, body.encode('utf-8'), header)
    response = con.getresponse()
    logger.info("Register monitor" + str(response.read().decode()))
    return web.Response(status=200, body='watting'.encode('utf-8'))


@asyncio.coroutine
def get_resource_description(request):
    app_id = request.match_info.get('app_id')
    # http://127.0.0.1:8080/~/mn-cse/mn-name/MY_SENSOR/DESCRIPTOR/ol
    resource_uri = '/~/' + 'mn-cse/mn-name' + '/' + app_id + '/' + 'DESCRIPTOR' + '/' + 'la'
    con = http.client.HTTPConnection(DOMAIN)
    header = {'X-M2M-Origin': 'admin:admin', "Content-type": "application/xml"}
    con.request('GET', resource_uri, '', header)
    response = con.getresponse()
    logger.info("Request: GET/URI:" + resource_uri)
    return web.Response(status=200, body=response.read().decode().encode('utf-8'))


@asyncio.coroutine
def switchON(request):
    time_delay = request.match_info.get('timeDelay')
    # /mn-cse/mn-name/TEMPERATURE_SENSOR?appId=TEMPERATURE_SENSOR&op=switchOn&timeDelay=0
    app_ids = ['TEMPERATURE_SENSOR', 'AIR_HUMIDITY_SENSOR', 'LIGHT_SENSOR']
    for app_id in app_ids:
        resource_uri = '/~/' + 'mn-cse/mn-name/' + app_id + '?appId=' + app_id + '&op=switchOn&timeDelay=' + str(
            time_delay)
        con = http.client.HTTPConnection(DOMAIN)
        header = {'X-M2M-Origin': 'admin:admin', "Content-type": "application/xml", "Connection": "close"}
        con.request('POST', resource_uri, '', header)
        # response = con.getresponse()
        # all_response += response.read().decode()
    all_response = 'waitting!'
    logger.info("Request: GET/URI:" + resource_uri)
    return web.Response(status=200, body=all_response.encode('utf-8'))


@asyncio.coroutine
def switchOFF(request):
    time_delay = request.match_info.get('timeDelay')
    # /mn-cse/mn-name/TEMPERATURE_SENSOR?appId=TEMPERATURE_SENSOR&op=switchOn&timeDelay=0
    app_ids = ['TEMPERATURE_SENSOR', 'AIR_HUMIDITY_SENSOR', 'LIGHT_SENSOR']
    all_response = ''
    for app_id in app_ids:
        resource_uri = '/~/' + 'mn-cse/mn-name/' + app_id + '?appId=' + app_id + '&op=switchOff&timeDelay=' + str(
            time_delay)
        con = http.client.HTTPConnection(DOMAIN)
        header = {'X-M2M-Origin': 'admin:admin', "Content-type": "application/xml", "Connection": "close"}
        con.request('POST', resource_uri, '', header)
        # response = con.getresponse()
        # all_response += response.read().decode()
    all_response = 'waitting!'
    logger.info("Request: GET/URI:" + resource_uri)
    return web.Response(status=200, body=all_response.encode('utf-8'))


@asyncio.coroutine
def monitor(request):
    data = yield from request.text()
    data = data.replace('&lt;', '<').replace('&quot;', '"')
    start_index = data.find('<obj>')
    end_index = data.find('</obj>')
    raw_data = data[start_index - 1:end_index + len('</obj>') + 1]
    logger.info(raw_data)
    if cloudAMPQclient.publish_message(data):
        logger.info('---> Publish message to CloudAMPQ')
    else:
        logger.info('---> Cant connect to AMPQ server')
    logger.info('---> Store data to influxdb')
    # influxdb_client.store_data(raw_data)
    logger.info('---> Export data to prometheus')
    prometheus_client.export_data(xml_data=raw_data)
    return web.Response(status=200, body=' '.encode('utf-8'))
    #     <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    # <obj>
    #     <str val="TEMPERATURE_SENSOR" name="appId"/>
    #     <str val="temperature" name="category"/>
    #     <int val="73" name="data"/>
    #     <str val="celsius" name="unit"/>
    # </obj>


@asyncio.coroutine
def tracking(request):
    logger.info('---> Cosume message from CloudAMPQ')
    message = cloudAMPQclient.consume_message()
    return web.Response(status=200, body=message.encode('utf-8'))


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    # Get resource description
    app.router.add_route('GET', '/resource/{app_id}/descriptor', get_resource_description)
    # Get resource state
    app.router.add_route('GET', '/resource/{app_id}/state', get_resource_state)
    # Get resources state
    app.router.add_route('GET', '/resource/all/state', get_all_resource_state)
    # Switch on all resource
    app.router.add_route('GET', '/all/resource/switchON?timeDelay={timeDelay}', switchON)
    # Switch off all resource
    app.router.add_route('GET', '/all/resource/switchOFF?timeDelay={timeDelay}', switchOFF)

    app.router.add_route('POST', '/monitor', monitor)

    app.router.add_route('GET', '/{oneM2M_host}/monitor/all/register', monitor_all_register)

    app.router.add_route('GET', '/monitor/register/{app_id}', monitor_register)

    srv = yield from loop.create_server(app.make_handler(), HOST, PORT)
    print("Server started at " + HOST + ":" + str(PORT))
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
