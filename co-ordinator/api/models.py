from django.conf import settings
from django.db import models

class DeploymentManager(models.Manager):

    def get_last_id(self):
        return super(DeploymentManager, self).get_queryset().count()

    # def get_sensor_config_not_assigned(self):
    #     return Deployment.objects.filter(platform_id='').first()

    def get_all_sensor_detail(self):
        items = Deployment.objects.get_queryset()
        list_items = list()
        for item in items:
            list_items.append({'sensor_id': item.sensor_id, 'sensor_ip': item.sensor_ip, 'config_path': item.sensor_config_path})
        return list_items

    def get_sensor_config_by_sensor_id(self, sensor_id):
        result = Deployment.objects.filter(sensor_id=sensor_id).first()
        if result:
            return result.sensor_config_path
        return None

    # def update_assign_sensor(self, sensor_id, platform_id, platform_ip):
    #     return super(DeploymentManager, self).get_queryset().filter(sensor_id=sensor_id)\
    #         .update(platform_id=platform_id, platform_ip=platform_ip)

    def get_sensor_detail_by_sensor_id(self, sensor_id):
        item = Deployment.objects.filter(sensor_id=sensor_id).first()
        if item:
            return {'sensor_id': item.sensor_id, 'sensor_ip': item.sensor_ip, 'config_path': item.sensor_config_path}
        return None

class Deployment(models.Model):
    id = models.IntegerField(primary_key=True)
    sensor_id = models.TextField(unique=True)
    sensor_ip = models.TextField()
    sensor_config_path = models.TextField()
    # platform_id = models.TextField(default='')
    # platform_ip = models.TextField(default='')
    objects = DeploymentManager()

