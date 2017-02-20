from django.conf.urls import url
from . import views
urlpatterns = [
    # url(r'^$', views.NewsSearchView.as_view(), name='es_search'),
    url(r'^sensor/create$', views.post_create_sensor, name='create_sensor'),
    url(r'^sensor/define$', views.post_receive_define_sensor, name='receive_define_sensor'),
    url(r'^platform/status$', views.post_receive_platform_success, name='receive_platform_success'),
]

