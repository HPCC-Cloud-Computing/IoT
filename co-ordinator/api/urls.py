from django.conf.urls import url
from . import views
urlpatterns = [
    # url(r'^$', views.NewsSearchView.as_view(), name='es_search'),
    url(r'^sensor$', views.SensorView.as_view(), name='sensor_request'),
    url(r'^sensor/register', views.SensorRegistrationView.as_view(), name='receive_define_sensor'),
    # url(r'^platform/status$', views.post_receive_platform_success, name='receive_platform_success'),
]

# url(r'^/(?P<fta_id>.+)/tariffs$', views.TariffsView.as_view(), name='tariffs'),