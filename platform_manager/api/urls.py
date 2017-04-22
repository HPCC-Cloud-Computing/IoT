from django.conf.urls import url
from . import views
urlpatterns = [
    # url(r'^$', views.NewsSearchView.as_view(), name='es_search'),
    url(r'^platform$', views.PlatformView.as_view(), name='sensor_request'),
    url(r'^platform/register$', views.PlatformRegistration.as_view(), name='sensor_request'),
    url(r'^platform/assignment', views.PlatformAssignment.as_view(), name='sensor_request'),
    # url(r'^platform/assignment/config', views.PlatformAssignment.post_receive_platform_register(), name='sensor_request'),
]

