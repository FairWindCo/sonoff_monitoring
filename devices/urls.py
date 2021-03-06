from django.urls import path

from devices.view_vue import main_view
from devices.views import list_device_status_ajax, device_history, list_device_status, device_status, \
    list_device_offline, device_graph, device_info, list_values, list_group_device, group_status_ajax, device_gaudge, \
    list_filtered_device_status_ajax, device_graph_ex, list_values_ex

urlpatterns = [
    path('status/', device_status, name='status'),
    path('gaudge/', device_gaudge, name='gaudge'),
    path('list/', list_device_status, name='list_devices'),
    path('offline/', list_device_offline, name='list_device_offline'),
    path('ajax_list/', list_device_status_ajax, name='ajax_list_devices'),
    path('ajax_filtered_list/', list_filtered_device_status_ajax, name='list_filtered_device_status_ajax'),
    path('history/<int:device_id>/', device_history, name='device_history'),
    path('history/<int:device_id>/<int:maxpoints>/', device_history, name='device_history'),
    path('info-<int:device_id>/', device_info, name='device_info'),
    path('list-values/', list_values_ex, name='list_values_ex'),
    path('values-<int:device_id>/', list_values, name='list_values'),
    path('graph-<int:device_id>/', device_graph, name='device_graph'),
    path('graphs/', device_graph_ex, name='graphs'),
    path('groups/', list_group_device, name='list_groups'),
    path('group-<int:device_group_id>/', list_group_device, name='list_group_device'),
    path('ajaxgroup-<int:group_id>/', group_status_ajax, name='group_status_ajax'),
    path('ajaxgroup/', list_device_status_ajax, name='group_status_ajax'),
    path('', list_device_status),
    path('main_vue/', main_view)
]
