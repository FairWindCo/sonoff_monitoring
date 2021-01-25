from datetime import timedelta

from django.http import JsonResponse
# Create your views here.
from django.template.response import TemplateResponse
from django.utils import formats
from django.utils import timezone

from devices.models import SonoffDevices, DeviceGroups
from utils.utils import paginate, request_paginator_form, get_request_param


def form_ajax_response(request, device_objects):
    devices, *_ = paginate(request, device_objects)
    status = []
    for device in devices:
        status.append({
            'id': device.id,
            'on_line': device.is_online,
            'name': device.name,
            'temperature': device.last_temperature,
            'humidity': device.last_humidity,
            'switch': device.switch,
            'last': formats.date_format(timezone.localtime(device.date_of_modify),
                                        'd M Y H:i:s') if device.is_online else formats.date_format(
                timezone.localtime(device.last_off_line), 'd M Y H:i:s'),
            'status_temp': device.temperature_status,
            'status_hum': device.humidity_status,
        })
    return JsonResponse(status, safe=False)


def list_device_status_ajax(request):
    return form_ajax_response(request, SonoffDevices.objects.all().order_by('pk'))


def group_status_ajax(request, group_id=None):
    if group_id is None:
        return list_device_status_ajax(request)

    device_group = DeviceGroups.objects.get(pk=group_id)
    return form_ajax_response(request, device_group.devices.all().order_by('pk'))


def list_group_device(request, device_group_id=None):
    groups = DeviceGroups.objects.all().order_by('name')
    devices = []
    device_group_name = ''
    current_id = None
    if device_group_id is None:
        devices = SonoffDevices.objects.all().order_by('pk')
    else:
        device_group = DeviceGroups.objects.get(pk=device_group_id)
        if device_group:
            current_id = device_group.id
            device_group_name = device_group.name
            devices = device_group.devices.all().order_by('pk')

    return request_paginator_form(request, 'devices/group_devices_status.html', devices,
                                  result_field_name='devices',
                                  groups=groups,
                                  device_group_name=device_group_name,
                                  current_id=current_id,
                                  )


def list_device_status(request):
    per_page_values = [1, 10, 25, 50, 100]
    return request_paginator_form(request, 'devices/list_devices.html', SonoffDevices.objects.all().order_by('pk'),
                                  result_field_name='devices',
                                  per_page_values=per_page_values,
                                  search_attributes={'id': 'device_id__icontains',
                                                     'name': 'name__icontains',
                                                     'checkbox_active_only': 'is_online'})


def device_info(request, device_id):
    device = SonoffDevices.objects.get(pk=device_id)
    return TemplateResponse(request, 'devices/devices_info.html', context={'device': device})


def device_graph(request, device_id):
    device = SonoffDevices.objects.get(pk=device_id)
    device_values = []
    labels = ''
    humidity = ''
    temperature = ''
    current_date = timezone.localtime() + timedelta(minutes=1)
    print(timezone.localtime())
    before_date = current_date - timedelta(days=1)

    from_date = get_request_param(request, 'from_date', before_date.strftime('%m/%d/%Y %I:%M %p'))
    end_date = get_request_param(request, 'end_date', current_date.strftime('%m/%d/%Y %I:%M %p'))

    if device:
        f_date = timezone.datetime.strptime(from_date, '%m/%d/%Y %I:%M %p')
        t_date = timezone.datetime.strptime(end_date, '%m/%d/%Y %I:%M %p')

        device_values = [(val.humidity, val.temperature, val.date_of_modify)
                         for val in
                         device.values.filter(date_of_modify__range=(f_date, t_date)).order_by('date_of_modify')]
        labels = ','.join([formats.date_format(timezone.localtime(i[2]), '"d M Y H:i:s"') for i in device_values])
        humidity = ','.join(['{:.2f}'.format(i[0]) if i[0] else '0' for i in device_values])
        temperature = ','.join(['{:.2f}'.format(i[1]) if i[1] else '0' for i in device_values])

    return TemplateResponse(request, 'devices/device_chart.html', context={'device': device,
                                                                           'labels': labels,
                                                                           'temperature': temperature,
                                                                           'humidity': humidity,
                                                                           'from_date': from_date,
                                                                           'end_date': end_date,
                                                                           'values': device_values})


def list_values(request, device_id):
    device = SonoffDevices.objects.get(pk=device_id)
    device_values = []
    per_page_values = [1, 10, 25, 50, 100]
    current_date = timezone.localtime() + timedelta(minutes=1)
    before_date = current_date - timedelta(days=1)
    from_date = get_request_param(request, 'from_date', before_date.strftime('%m/%d/%Y %I:%M %p'))
    end_date = get_request_param(request, 'end_date', current_date.strftime('%m/%d/%Y %I:%M %p'))

    if device:
        f_date = timezone.datetime.strptime(from_date, '%m/%d/%Y %I:%M %p')
        t_date = timezone.datetime.strptime(end_date, '%m/%d/%Y %I:%M %p')

        device_values = device.values.filter(date_of_modify__range=(f_date, t_date)).order_by('date_of_modify')

    return request_paginator_form(request, 'devices/list_values.html',
                                  device_values,
                                  result_field_name='values',
                                  per_page_values=per_page_values,
                                  additional_fields={
                                      'from_date': from_date,
                                      'end_date': end_date,
                                  },
                                  # from_date=from_date,
                                  # end_date=end_date,
                                  device=device
                                  )
    # return TemplateResponse(request, 'devices/list_values.html', context={'device': device,
    #                                                                        'from_date':from_date,
    #                                                                        'end_date':end_date,
    #                                                                        'values': device_values})


def list_device_offline(request):
    per_page_values = [1, 10, 25, 50, 100]
    return request_paginator_form(request, 'devices/list_offline_devices.html',
                                  SonoffDevices.objects.filter(is_online=False).order_by('pk'),
                                  result_field_name='devices',
                                  per_page_values=per_page_values,
                                  search_attributes={'id': 'device_id__icontains',
                                                     'name': 'name__icontains'})


def device_gaudge(request):
    return request_paginator_form(request, 'devices/devices_status_gaudge.html', SonoffDevices.objects.all().order_by('pk'),
                                  result_field_name='devices',
                                  search_attributes={'id': 'device_id__icontains',
                                                     'name': 'name__icontains'})


def device_status(request):
    return request_paginator_form(request, 'devices/devices_status.html', SonoffDevices.objects.all().order_by('pk'),
                                  result_field_name='devices',
                                  search_attributes={'id': 'device_id__icontains',
                                                     'name': 'name__icontains'})


def device_history(request, device_id, maxpoints=100):
    device = SonoffDevices.objects.get(pk=device_id)
    status = {}
    if device:
        device_values = [(val.humidity, val.temperature, val.switch, val.date_of_modify)
                         for val in device.values.all().order_by('-date_of_modify')[:maxpoints]]

        status = {
            'id': device.id,
            'on_line': device.is_online,
            'name': device.name,
            'temperature': device.last_temperature,
            'humidity': device.last_humidity,
            'switch': device.switch,
            'history': device_values
        }

    print(status)
    return JsonResponse(status)
