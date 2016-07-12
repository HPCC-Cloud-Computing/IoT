#! /usr/bin/env python3
__author__ = 'huanpc'

import asyncio

import json

import http.client

from aiohttp import web

import logging

import sys

import cloudAMPQclient

PROTOCOL = 'http'
HOST = '127.0.0.1'
PORT = '9090'
M2M_HOST = '127.0.0.1'
M2M_PORT = '8080'
DOMAIN = M2M_HOST + ':' + M2M_PORT

logger = logging.getLogger('RESOURCE_TRACKING')
logging.basicConfig(stream=sys.stderr, level=getattr(logging, 'INFO'))


@asyncio.coroutine
def get_resource_state(request):
    app_id = request.match_info.get('app_id')
    # 'http://127.0.0.1:8080/~/mn-cse/mn-name/LAMP_0/DATA/la'
    resource_uri = '/~/' + 'mn-cse/mn-name' + '/' + app_id + '/' + 'DATA' + '/' + 'la'
    con = http.client.HTTPConnection(DOMAIN)
    header = {'X-M2M-Origin': 'admin:admin', "Content-type": "application/xml"}
    con.request('GET', resource_uri, '', header)
    response = con.getresponse()
    logger.info("Request: GET/URI:" + resource_uri)
    return web.Response(status=200, body=response.read().decode().encode('utf-8'))

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
def switchON_lamp(request):
    app_id = request.match_info.get('app_id')
    # /mn-cse/mn-name/LAMP_0?op=setOn&lampid=LAMP_0
    resource_uri = '/~/' + 'mn-cse/mn-name/' + app_id + '?op=setOn&lampid=' + app_id
    con = http.client.HTTPConnection(DOMAIN)
    header = {'X-M2M-Origin': 'admin:admin', "Content-type": "application/xml"}
    con.request('POST', resource_uri, '', header)
    response = con.getresponse()
    logger.info("Request: GET/URI:" + resource_uri)
    return web.Response(status=200, body=response.read().decode().encode('utf-8'))

@asyncio.coroutine
def switchOFF_lamp(request):
    app_id = request.match_info.get('app_id')
    # /mn-cse/mn-name/LAMP_0?op=setOff&lampid=LAMP_0
    resource_uri = '/~/' + 'mn-cse/mn-name/' + app_id + '?op=setOff&lampid=' + app_id
    con = http.client.HTTPConnection(DOMAIN)
    header = {'X-M2M-Origin': 'admin:admin', "Content-type": "application/xml"}
    con.request('POST', resource_uri, '', header)
    response = con.getresponse()
    logger.info("Request: GET/URI:" + resource_uri)
    return web.Response(status=200, body=response.read().decode().encode('utf-8'))

@asyncio.coroutine
def monitor(request):
    data = yield from request.text()
    logger.info('---> Publish message to CloudAMPQ')
    cloudAMPQclient.publish_message(data)
    return web.Response(status=204, body=' '.encode('utf-8'))

@asyncio.coroutine
def tracking(request):
    logger.info('---> Cosume message from CloudAMPQ')
    message = cloudAMPQclient.consume_message()
    return web.Response(status=200, body=message.encode('utf-8'))

# @asyncio.coroutine
# def create_application_entity(request):
#     uri = 'http://127.0.0.1:8080/~/in-cse'
#     method = 'POST'
#     headers = {'X-M2M-Origin': 'admin:admin', 'Content-Type': 'application/xml;ty=2', 'X-M2M-NM': 'MY_SENSOR'}
#     body = '''
#     <om2m:ae xmlns:om2m="http://www.onem2m.org/xml/protocols">
#         <api>app-sensor</api>
#         <lbl>Type/sensor Category/temperature Location/home</lbl>
#         <rr>false</rr>
#     </om2m:ae>
#     '''
#     con = http.client.HTTPConnection(DOMAIN)
#     con.request(method, uri, '', headers)
#     response = con.getresponse()
#     logger.info("Request: POST/URI:" + uri)
#     return web.Response(status=200, body=response.read().decode().encode('utf-8'))

@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    # Get resource description
    app.router.add_route('GET', '/resource/{app_id}/descriptor', get_resource_description)
    # Get resource state
    app.router.add_route('GET', '/resource/{app_id}/state', get_resource_state)
    # Switch on lamp resource
    app.router.add_route('GET', '/resource/{app_id}/switchON', switchON_lamp)
    # Switch off lamp resource
    app.router.add_route('GET', '/resource/{app_id}/switchOFF', switchOFF_lamp)

    app.router.add_route('POST', '/monitor', monitor)

    srv = yield from loop.create_server(app.make_handler(), HOST, PORT)
    print("Server started at " + HOST + ":" + str(PORT))
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
