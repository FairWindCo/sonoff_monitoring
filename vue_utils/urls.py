from django.urls import path

from devices.views import list_device_status_ajax, device_history, list_device_status, device_status, \
    list_device_offline, device_graph, device_info, list_values, list_group_device, group_status_ajax, device_gaudge
from vue_utils.views import view_test

urlpatterns = [
    path('test/', view_test, name='test_base_vue'),
]
