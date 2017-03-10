from django.conf import settings
from django.db import models


class PlatformDeploymentModelManager(models.Manager):
    def get_platform_detail_by_id(self, platform_id):
        result = PlatformDeploymentModel.objects.filter(platform_id=platform_id).first()
        if result:
            return {'platform_id': result.platform_id, 'platform_ip': result.platform_ip}
        return None

    def get_all_platform_detail(self):
        items = PlatformDeploymentModel.objects.get_queryset()
        list_items = list()
        for item in items:
            list_items.append({'platform_id': item.platform_id, 'platform_ip': item.platform_ip})
        return list_items


class PlatformAssignmentModelManager(models.Manager):
    def create_assignment(self, sensor_id, platform_id):
        return

    def update_assignment_by_sensor_id(self, sensor_id, platform_id, assign_status):
        return super(PlatformAssignmentModelManager, self).get_queryset().filter(sensor_id=sensor_id)\
            .update(platform_id=platform_id, assign_status=assign_status)

    def update_assigment_status(self, sensor_id, platform_id, assign_status):
        return super(PlatformAssignmentModelManager, self).get_queryset().filter(sensor_id=sensor_id) \
            .filter(platform_id=platform_id) \
            .update(assign_status=assign_status)

    def delete_assignment_by_sensor_id(self, sensor_id):
        return

    def get_all_assignment(self):
        items = PlatformAssignmentModel.objects.get_queryset()
        list_items = list()
        for item in items:
            list_items.append({'platform_id': item.platform_id, 'platform_ip': item.platform_ip,
                               'sensor_id': item.sensor_id, 'sensor_ip': item.sensor_ip})
        return list_items

    def get_sensor_not_assign(self):
        # first in first serve
        result = PlatformAssignmentModel.objects.filter(platform_id='').first()
        if result:
            return result.sensor_id
        return None

    def get_sensor_id_assigned_temp(self, status, platform_id):
        result =  super(PlatformAssignmentModelManager, self).get_queryset().filter(platform_id=platform_id) \
            .filter(assign_status=status) \
            .first()
        if result:
            return result.sensor_id
        return None



class PlatformDeploymentModel(models.Model):
    id = models.IntegerField(primary_key=True)
    platform_id = models.TextField(unique=True)
    platform_ip = models.TextField()
    objects = PlatformDeploymentModelManager()
    pass


class PlatformAssignmentModel(models.Model):
    id = models.IntegerField(primary_key=True)
    sensor_id = models.TextField(unique=True)
    # sensor_ip = models.TextField()
    platform_id = models.TextField(unique=True)
    # platform_ip = models.TextField()
    # 0: temp, 1: active
    assign_status = models.IntegerField(default=0)
    objects = PlatformAssignmentModelManager()