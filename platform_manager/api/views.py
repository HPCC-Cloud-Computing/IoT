from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from . import models
# from .utils import restrict_search
from django.http import HttpResponse
import json
import http.client
import os.path
from wsgiref.util import FileWrapper
from .models import *
from influxdb import InfluxDBClient

KUBE_API_DOMAIN = '128.199.242.5:8080'
SENSOR_ORDINATOR_SERVICE_HOST = 'localhost:9090'
CONTENT_TYPE = {'JSON': "application/json", 'TEXT': 'text/plain'}
RESPONSE_JSON_TYPE_DEFINE = 'JSON'
RESPONSE_TEXT_TYPE_DEFINE = 'TEXT'

# ------------------------------------------------------------------------------------
# Exposed service
# ------------------------------------------------------------------------------------
# CRUD with platform
class PlatformView(APIView):
    @csrf_exempt
    def get(self, request):
        message = self._get_platform(request)
        return HttpResponse(json.dumps({"status": "ok", "message": message}), content_type="application/json")

    @csrf_exempt
    def post(self, request):
        message = self._deploy_platform()
        return HttpResponse(json.dumps({"status": "ok", "message": message}), content_type="application/json")

    # TODO
    @csrf_exempt
    def put(self, request):
        pass

    @csrf_exempt
    def delete(self, request):
        if request.DELETE.get('platform_id'):
            platform_id = request.DELETE.get('sensor_id')
            message = self._delete_sensor(platform_id=platform_id)
            return HttpResponse(json.dumps({"status": "ok", "message": message}), content_type="application/json")

    def _get_platform(self, request):
        if request.GET.get('platform_id'):
            platform_id = request.GET.getid('platform_id')
            platform_detail = PlatformDeploymentModel.objects.get_platform_detail_by_id(platform_id=platform_id)
            if platform_detail:
                return HttpResponse(json.dumps({"status": "ok", "message": platform_detail}), content_type='text/plain')
            return success_response(message="This platform is not existed")
        else:
            platform_details = PlatformDeploymentModel.objects.get_all_platform_detail()
            return HttpResponse(json.dumps({"status": "ok", "message": platform_details}), content_type='text/plain')

    def _deploy_platform(self):
        return deploy_platform()

    def _delete_sensor(self, platform_id):
        # /api/v1/namespaces/kube-system/replicationcontrollers/openhab-platform
        namespace = 'kube-system'
        uri_api = '/api/v1/namespaces/{namespace}/replicationcontrollers/{platform_id}'.format(namespace=namespace,
                                                                                               platform_id=platform_id)
        con = http.client.HTTPConnection(KUBE_API_DOMAIN)
        header = {"Content-type": "application/json"}
        con.request('DELETE', uri_api, '', header)
        response = con.getresponse()
        raw = response.read().decode()
        return raw

    def _scale_platform(self):
        return scale_platform()


class PlatformRegistration(APIView):
    def get(self, request):
        '''
        register platform (temp use this replace for post method)
        :param request:
        :return:
        '''
        data = dict(request.GET)
        if data.get('platform'):
            ### register to PR
            platform_detail = data['platform'][0].split(',')
            cluster_ip = platform_detail[0]
            platform_id = platform_detail[1]
            # add to db
            item = PlatformDeploymentModel(platform_id=platform_id, platform_ip=cluster_ip)
            item.save()
            ### register to PA
            message = assign_sensor_for_platform(platform_id=platform_id)
            return success_response(message=message)
        # get all registration
        message = PlatformAssignmentModel.objects.get_all_assignment()
        return success_response(message)

    def post(self, request):
        '''
        register platform
        :param request:
        :return:
        '''
        return

# TODO
class PlatformAssignment(APIView):
    def put(self, request):
        assign_status = request.PUT.get('assign_status')[0]
        platform_detail = request.PUT.get('platform')[0].split(',')
        sensor_id = request.PUT.get('sensor_id')[0]
        platform_id = platform_detail[1]
        # post_receive_platform_register
        # update db, change temp -> active
        message = PlatformAssignmentModel.objects.update_assigment_status(sensor_id=sensor_id, platform_id=platform_id,
                                                                assign_status=1)
        return success_response(message)

    def post(self, request):
        # post_receive_sensor_register
        data = dict(request.POST)
        sensor_id = data['sensor_id'][0]
        # create assignment
        item = PlatformAssignmentModel(sensor_id=sensor_id, platform_id='')
        item.save()
        return success_response()

    def get(self, request):
        # get_get_sensor_assign_with_platform
        '''
        return sensor config assigned with platform
        :param: platform id
        :return: file config
        '''
        platform_detail = request.GET.get('platform').split(',')
        platform_id = platform_detail[1]
        resource_type = request.GET.get('resource')
        # Goi len platform assign tim nhung thang co temp assign platform, roi tra ve sensor define
        if resource_type and resource_type == 'config_file':
            sensor_id = request.GET.get('sensor_id')
            # call to co-ordinator de lay config
            uri = '/sensor/register?sensor_id={sensor_id}&resource=defined_file'.format(sensor_id=sensor_id)
            # localhost:9090/sensor/register?sensor_id=sensor_1&resource=defined_file
            con = http.client.HTTPConnection(SENSOR_ORDINATOR_SERVICE_HOST)
            header = {"Content-type": "text/plain"}
            con.request('GET', uri, '', header)
            response = con.getresponse()
            raw = response.read()
            response = HttpResponse(raw, content_type='text/plain')
            response['Content-Length'] = len(raw)
            return response

        # Goi len platform assign tim nhung thang co temp assign platform, roi tra ve sensor id
        if resource_type and resource_type == 'sensor_id':
            message = PlatformAssignmentModel.objects.get_sensor_id_assigned_temp(status=0, platform_id=platform_id)
            response = HttpResponse(message, content_type='text/plain')
            response['Content-Length'] = len(message)
            return response
        action = request.GET.get('action')
        if action and action == 'register_succeed':
            sensor_id = request.GET.get('sensor_id')
            if platform_id and sensor_id:
                # update db, change temp -> active
                message = PlatformAssignmentModel.objects.update_assigment_status(sensor_id=sensor_id,
                                                                                  platform_id=platform_id,
                                                                                  assign_status=1)
                return success_response(message=message)

# ------------------------------------------------------------------------------------
# Daemon service
# ------------------------------------------------------------------------------------
# TODO
class Scheduler:

    def engine_scheduler(self):
        # TODO: - collect platform monitored metric - scale and assign node for platform - re-assign platform for sensor
        return

    def _collect_metric_data(self):

        client = InfluxDBClient('188.166.238.158', 32485, 'root', 'root', 'k8s')
        result = client.query('SELECT sum("value") FROM "memory/usage" WHERE "type" = \'node\' AND time > now() - 1d GROUP BY time(1d), "nodename" fill(null);')
        # ('memory/usage', {'nodename': '128.199.242.5'}) - - [{'sum': 1275429384192, 'time': '2017-02-25T00:00:00Z'},
        #                                                      {'sum': 1038484692992, 'time': '2017-02-26T00:00:00Z'}]
        return

    def _get_platform(self):
        pass

    def _deploy_platform(self):
        return deploy_platform()

    def _deploy_scale_platform(self):
        return scale_platform()

    def _delete_platform(self):
        pass

    def _scale_platform(self):
        pass


# ------------------------------------------------------------------------------------
# Utils function
# ------------------------------------------------------------------------------------
def deploy_platform():
    namespace = 'kube-system'
    platform_name = 'openhab-platform'
    platform_config = 'openhab-cfg'
    co_ordinator_config_name = 'CO_ORDINATOR_DOMAIN'
    node_selector = {"fog_node": "worker_1"}
    deploy_api = '/api/v1/namespaces/{namespace}/replicationcontrollers'.format(namespace=namespace)
    con = http.client.HTTPConnection(KUBE_API_DOMAIN)
    header = {"Content-type": "application/json"}
    body = {
        "kind": "ReplicationController",
        "apiVersion": "v1",
        "metadata": {
            "name": platform_name,
            "namespace": "kube-system"
        },
        "spec": {
            "replicas": 1,
            "selector": {"app": platform_name},
            "template": {
                "metadata": {
                    "name": platform_name,
                    "labels": {"app": platform_name}
                },
                "spec": {
                    "containers": [{
                        "name": platform_name,
                        "image": "huanphan/openhab:0.3",
                        # "ports": [
                        #     {
                        #         "hostPort": 8080,
                        #         "containerPort": 8080
                        #     }
                        # ],
                        "volumeMounts": [
                            {
                                "name": platform_config,
                                "mountPath": "/openhab/configurations/openhab.cfg",
                                "subPath": "openhab.cfg"
                            }
                        ],
                        "env": [
                            {
                                "name": co_ordinator_config_name,
                                "valueFrom": {
                                    "configMapKeyRef": {
                                        "name": "co-ordinator-config",
                                        "key": "co-ordinator.domain"
                                    }
                                }
                            }
                        ]
                    }],
                    "volumes": [{
                        "name": platform_config,
                        "configMap": {
                            "name": platform_config
                        }
                    }],
                    "restartPolicy": "Always",
                    "nodeSelector": node_selector
                }
            }
        }
    }
    con.request('POST', deploy_api, json.dumps(body).encode('utf-8'), header)
    response = con.getresponse()
    raw = response.read().decode()
    return raw


def scale_platform():
    # get current replicas
    platform_name = 'openhab-platform'
    namespace = 'kube-system'
    platform_config = 'openhab-cfg'
    co_ordinator_config_name = 'CO_ORDINATOR_DOMAIN'
    node_selector = {"fog_node": "worker_1"}
    con = http.client.HTTPConnection(KUBE_API_DOMAIN)
    header = {"Content-type": "application/json"}
    uri = '/api/v1/namespaces/{namespace}/replicationcontrollers/{name}/scale'.format(namespace=namespace,
                                                                                      name=platform_name)
    con.request('GET', uri, '', header)
    response = con.getresponse()
    data = json.loads(response.read().decode())
    # if there aren't any platform instance, then we create a new one
    if not data.get('spec', ''):
        print(deploy_platform())
        return 1
    current_replicas = data['spec']['replicas']
    # scale
    # uri = '/api/v1/proxy/namespaces/{namespace}/services/kubernetes-dashboard' \
    #       '/api/v1/replicationcontroller/{namespace}/{name}/update/pod'.format(namespace=namespace,
    #                                                                            name=platform_name)
    # body = {
    #     'replicas': current_replicas + 1
    # }
    uri = '/api/v1/namespaces/{namespace}/replicationcontrollers/{platform_name}'.format(namespace=namespace,
                                                                                         platform_name=platform_name)
    body = {
        "kind": "ReplicationController",
        "apiVersion": "v1",
        "metadata": {
            "name": platform_name,
            "namespace": "kube-system"
        },
        "spec": {
            "replicas": int(current_replicas+1),
            "selector": {"app": platform_name},
            "template": {
                "metadata": {
                    "name": platform_name,
                    "labels": {"app": platform_name}
                },
                "spec": {
                    "containers": [{
                        "name": platform_name,
                        "image": "huanphan/openhab:0.3",
                        # "ports": [
                        #     {
                        #         "hostPort": 8080,
                        #         "containerPort": 8080
                        #     }
                        # ],
                        "volumeMounts": [
                            {
                                "name": platform_config,
                                "mountPath": "/openhab/configurations/openhab.cfg",
                                "subPath": "openhab.cfg"
                            }
                        ],
                        "env": [
                            {
                                "name": co_ordinator_config_name,
                                "valueFrom": {
                                    "configMapKeyRef": {
                                        "name": "co-ordinator-config",
                                        "key": "co-ordinator.domain"
                                    }
                                }
                            }
                        ]
                    }],
                    "volumes": [{
                        "name": platform_config,
                        "configMap": {
                            "name": platform_config
                        }
                    }],
                    "restartPolicy": "Always",
                    "nodeSelector": node_selector
                }
            }
        }
    }
    con.request('POST', uri, json.dumps(body).encode('utf-8'), header)
    response = con.getresponse()
    if response.read().decode() == '':
        return current_replicas + 1
    return False


def assign_sensor_for_platform(platform_id):
    # TODO: - assign platform for sensor by two algorithm: + round-robin + first-in first-serve
    # Get sensor id
    sensor_id = PlatformAssignmentModel.objects.get_sensor_not_assign()
    # update tam thoi
    message = PlatformAssignmentModel.objects.update_assignment_by_sensor_id(sensor_id=sensor_id,
                                                                          platform_id=platform_id, assign_status=0)
    return message

# TODO
def assign_platform_on_node():
    # collect monitor metric from node
    # schedule
    return


def success_response(message='No message'):
    return HttpResponse(json.dumps({"status": "ok", "message": message}), content_type="application/json")

def error_response(message='No message'):
    return HttpResponse(json.dumps({"status": "error", "message": message}), content_type="application/json")

# client = InfluxDBClient('188.166.238.158', 32485, 'root', 'root', 'k8s')
# client.query('SELECT sum("value") FROM "memory/usage" WHERE "type" = \'node\' AND "nodename" = \'128.199.242.5\'  AND time > now() - 1d GROUP BY time(10m), "nodename" fill(null);')