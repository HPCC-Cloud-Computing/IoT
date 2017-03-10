from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from . import models
# from .utils import restrict_search
from django.http import HttpResponse
from rest_framework.response import Response
import json
import http.client
import os.path
from wsgiref.util import FileWrapper
from .models import *

KUBE_API_DOMAIN = '128.199.242.5:8080'

# CRUD with sensor
class SensorView(APIView):
    @csrf_exempt
    def get(self, request):
        message = self.get_sensor(request=request)
        return message

    @csrf_exempt
    def post(self, request):
        message = self._deploy_sensor()
        return HttpResponse(json.dumps({"status": "ok", "message": message}), content_type="application/json")

    @csrf_exempt
    def put(self, request):
        pass

    @csrf_exempt
    def delete(self, request):
        if request.DELETE.get('sensor_id'):
            sensor_id = request.DELETE.get('sensor_id')
            message = self._delete_sensor(sensor_id=sensor_id)
            return HttpResponse(json.dumps({"status": "ok", "message": message}), content_type="application/json")

    def get_sensor(self, request):
        if request.GET.get('sensor_id'):
            sensor_id = request.GET.get('sensor_id')
            if request.GET.get('resource') == 'defined_file':
                result = Deployment.objects.get_sensor_config_by_sensor_id(sensor_id)
                if result:
                    wrapper = FileWrapper(open(result, 'r'))
                    response = HttpResponse(wrapper, content_type='text/plain')
                    response['Content-Length'] = os.path.getsize(result)
                    return response
            sensor_detail = Deployment.objects.get_sensor_detail_by_sensor_id(sensor_id)
            if sensor_detail:
                return HttpResponse(json.dumps({"status": "ok", "message": sensor_detail}), content_type='text/plain')
            return HttpResponse(json.dumps({"status": "error", "message": "This sensor is not existed"}),
                                content_type="application/json")
        else:
            sensor_details = Deployment.objects.get_all_sensor_detail()
            return HttpResponse(json.dumps({"status": "ok", "message": sensor_details}), content_type='text/plain')

    def _deploy_sensor(self):
        namespace = 'kube-system'
        # gen sensor name
        sensor_name = 'sensor-gen-{}'.format(Deployment.objects.get_last_id())
        # create config map
        # POST /api/v1/namespaces/{namespace}/configmaps
        # TODO auto gen new config map
        # for now, i just use this fixed value
        sensor_config = 'sensor-config'
        co_ordinator_config_name = 'CO_ORDINATOR_DOMAIN'
        docker_image = "huanphan/sensor-simulator:0.5"
        # create sensor
        # POST / api / v1 / namespaces / {namespace} / replicationcontrollers
        deploy_api = '/api/v1/namespaces/{namespace}/replicationcontrollers'.format(namespace=namespace)
        con = http.client.HTTPConnection(KUBE_API_DOMAIN)
        header = {"Content-type": "application/json"}
        body = {
            "kind": "ReplicationController",
            "apiVersion": "v1",
            "metadata": {
                "name": sensor_name,
                "namespace": "kube-system"
            },
            "spec": {
                "replicas": 1,
                "selector": {"app": sensor_name},
                "template": {
                    "metadata": {
                        "name": sensor_name,
                        "labels": {"app": sensor_name}
                    },
                    "spec": {
                        "containers": [{
                            "name": sensor_name,
                            "image": docker_image,
                            "volumeMounts": [
                                {
                                    "name": sensor_name,
                                    "mountPath": "/SimulateSensor/config"
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
                            "name": sensor_name,
                            "configMap": {
                                "name": sensor_config,
                                "items": [{
                                    "key": "config.cfg",
                                    "path": "config.cfg"
                                }]
                            }
                        }],
                        "restartPolicy": "Always"
                    }
                }
            }
        }
        con.request('POST', deploy_api, json.dumps(body).encode('utf-8'), header)
        response = con.getresponse()
        raw = response.read().decode()
        return raw

    def _delete_sensor(self, sensor_id):
        # /api/v1/namespaces/kube-system/replicationcontrollers/openhab-platform
        namespace = 'kube-system'
        uri_api = '/api/v1/namespaces/{namespace}/replicationcontrollers/{sensor_name}'.format(namespace=namespace, sensor_id=sensor_id)
        con = http.client.HTTPConnection(KUBE_API_DOMAIN)
        header = {"Content-type": "application/json"}
        con.request('DELETE', uri_api, '', header)
        response = con.getresponse()
        raw = response.read().decode()
        return raw

    def _update_sensor(self):
        pass

class SensorRegistrationView(APIView):
    @csrf_exempt
    def get(self, request):
        return SensorView().get_sensor(request=request)
        # if request.GET.get('sensor_id'):
        #     sensor_id = request.GET.get('sensor_id')
        #     if request.GET.get('resource') == 'defined_file':
        #         result = Deployment.objects.get_sensor_config_by_sensor_id(sensor_id)
        #         if result:
        #             wrapper = FileWrapper(open(result, 'r'))
        #             response = HttpResponse(wrapper, content_type='text/plain')
        #             response['Content-Length'] = os.path.getsize(result)
        #             return response
        #     sensor_detail = Deployment.objects.get_sensor_config_by_sensor_id(sensor_id)
        #     if sensor_detail:
        #         return HttpResponse(json.dumps(dict(sensor_detail)), content_type='text/plain')
        # return HttpResponse(json.dumps({"status": "error", "message": "This sensor is not existed"}), content_type="application/json")

    @csrf_exempt
    def post(self, request):
        data = dict(request.POST)
        sensor_detail = data['sensor_detail'][0].split(',')
        sensor_ip = sensor_detail[0]
        sensor_id = sensor_detail[1]
        file_path = 'sensor_define/' + 'config_{}.cfg'.format(sensor_id)
        # upload file
        upload_file(request.FILES.get('defined_file'), file_path)
        # add to db
        item = Deployment(sensor_id=sensor_id, sensor_config_path=file_path, platform_id='', sensor_ip=sensor_ip)
        item.save()
        count_sensor = 1
        message = {"status": "ok", "message": "Num of sensor {}".format(count_sensor)}
        return HttpResponse(json.dumps(message), content_type="application/json")

# @csrf_exempt
# def post_receive_sensor_config(request):
#     if request.method == 'POST':
#         data = dict(request.POST)
#         sensor_detail = data['sensor_detail'][0].split(',')
#         sensor_ip = sensor_detail[0]
#         sensor_id = sensor_detail[1]
#         file_path = 'sensor_define/' + 'config_{}.cfg'.format(sensor_id)
#         # upload file
#         upload_file(request.FILES.get('defined_file'), file_path)
#         # add to db
#         item = Deployment(sensor_id=sensor_id, sensor_config_path=file_path, platform_id='', sensor_ip=sensor_ip)
#         item.save()
#         # message = {"status": "error", "message": "Cannot scale platform"}
#         # if there aren't any platform instance, then we create a new one
#         # or we just scale this platform
#         replicas = deploy_scale_platform()
#         if replicas:
#             message = {"status": "ok", "message": "Num of replicas: {}".format(replicas)}
#         return HttpResponse(json.dumps(message), content_type="application/json")
#     elif request.method == 'GET':
#         if request.GET.get('resource') == 'defined_file':
#             result = Deployment.objects.get_sensor_config_not_assigned()
#             if result:
#                 path_file_dest = result.sensor_config_path
#                 wrapper = FileWrapper(open(path_file_dest, 'r'))
#                 response = HttpResponse(wrapper, content_type='text/plain')
#                 response['Content-Length'] = os.path.getsize(path_file_dest)
#                 return response
#         elif request.GET.get('resource') == 'sensor_id':
#             result = Deployment.objects.get_sensor_config_not_assigned()
#             if result:
#                 message = result.sensor_id
#                 return HttpResponse(message, content_type="text/plain")
#
#     return HttpResponse(json.dumps({"status": "error", "message": "Invalid Method"}),
#                             content_type="application/json")

def upload_file(file, file_path):
    path_file_dest = file_path
    with open(path_file_dest, "wb") as myfile:
        byte = file.read(1)
        while byte != b"":
            myfile.write(byte)
            byte = file.read(1)
    if os.path.isfile(path_file_dest):
        return path_file_dest
    return False

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

# ---------------------------------------------
# def deploy_platform():
#     namespace = 'kube-system'
#     platform_name = 'openhab-platform'
#     platform_config = 'openhab-cfg'
#     co_ordinator_config_name = 'CO_ORDINATOR_DOMAIN'
#     deploy_api = '/api/v1/namespaces/{namespace}/replicationcontrollers'.format(namespace=namespace)
#     con = http.client.HTTPConnection(KUBE_API_DOMAIN)
#     header = {"Content-type": "application/json"}
#     body = {
#         "kind": "ReplicationController",
#         "apiVersion": "v1",
#         "metadata": {
#             "name": platform_name,
#             "namespace": "kube-system"
#         },
#         "spec": {
#             "replicas": 1,
#             "selector": {"app": platform_name},
#             "template": {
#                 "metadata": {
#                     "name": platform_name,
#                     "labels": {"app": platform_name}
#                 },
#                 "spec": {
#                     "containers": [{
#                         "name": platform_name,
#                         "image": "huanphan/openhab:0.3",
#                         # "ports": [
#                         #     {
#                         #         "hostPort": 8080,
#                         #         "containerPort": 8080
#                         #     }
#                         # ],
#                         "volumeMounts": [
#                             {
#                                 "name": platform_config,
#                                 "mountPath": "/openhab/configurations/openhab.cfg",
#                                 "subPath": "openhab.cfg"
#                             }
#                         ],
#                         "env": [
#                             {
#                                 "name": co_ordinator_config_name,
#                                 "valueFrom": {
#                                     "configMapKeyRef": {
#                                         "name": "co-ordinator-config",
#                                         "key": "co-ordinator.domain"
#                                     }
#                                 }
#                             }
#                         ]
#                     }],
#                     "volumes": [{
#                         "name": platform_config,
#                         "configMap": {
#                             "name": platform_config
#                         }
#                     }],
#                     "restartPolicy": "Always"
#                 }
#             }
#         }
#     }
#     con.request('POST', deploy_api, json.dumps(body).encode('utf-8'), header)
#     response = con.getresponse()
#     raw = response.read().decode()
#     return raw

# def deploy_scale_platform():
#     # get current replicas
#     platform_name = 'openhab-platform'
#     namespace = 'kube-system'
#     con = http.client.HTTPConnection(KUBE_API_DOMAIN)
#     header = {"Content-type": "application/json"}
#     uri = '/api/v1/namespaces/{namespace}/replicationcontrollers/{name}/scale'.format(namespace=namespace, name=platform_name)
#     con.request('GET', uri, '', header)
#     response = con.getresponse()
#     data = json.loads(response.read().decode())
#     # if there aren't any platform instance, then we create a new one
#     if not data.get('spec', ''):
#         print(deploy_platform())
#         return 1
#     current_replicas = data['spec']['replicas']
#     # scale
#     uri = '/api/v1/proxy/namespaces/{namespace}/services/kubernetes-dashboard' \
#           '/api/v1/replicationcontroller/{namespace}/{name}/update/pod'.format(namespace=namespace, name=platform_name)
#     body = {
#         'replicas': current_replicas+1
#     }
#     con.request('POST', uri, json.dumps(body).encode('utf-8'), header)
#     response = con.getresponse()
#     if response.read().decode() == '':
#         return current_replicas + 1
#     return False

# @csrf_exempt
# def post_receive_platform_success(request):
#     if request.method == 'GET':
#         data = dict(request.GET)
#         platform_detail = data['platform'][0].split('-')
#         cluster_ip = platform_detail[0]
#         platform_id = platform_detail[1]
#         sensor_id = data['sensor_id'][0]
#         # add to db
#         Deployment.objects.update_assign_sensor(sensor_id=sensor_id, platform_id=platform_id, platform_ip=cluster_ip)
#         return HttpResponse(json.dumps({"status": "ok", "message": "success"}), content_type="application/json")

# ---------------------------------------------