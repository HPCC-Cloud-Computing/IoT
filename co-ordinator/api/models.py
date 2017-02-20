from django.conf import settings
from django.db import models

class DeploymentManager(models.Manager):

    def get_last_id(self):
        return super(DeploymentManager, self).get_queryset().count()

    def get_sensor_config_not_assigned(self):
        # StaffTracking.objects.filter(action_type=action_type)
        return Deployment.objects.filter(platform_id='').first()
        # return super(DeploymentManager, self).get_queryset().filter(platform_id='')

    def update_assign_sensor(self, sensor_id, platform_id, platform_ip):
        return super(DeploymentManager, self).get_queryset().filter(sensor_id=sensor_id)\
            .update(platform_id=platform_id, platform_ip=platform_ip)

class Deployment(models.Model):
    id = models.IntegerField(primary_key=True)
    sensor_id = models.TextField()
    sensor_ip = models.TextField()
    sensor_config_path = models.TextField()
    platform_id = models.TextField(default='')
    platform_ip = models.TextField(default='')
    objects = DeploymentManager()

