from django.http import JsonResponse
from django.shortcuts import render

from devices.models import SonoffDevices


def form_ajax_device_conf(request):
    list_devices = list(SonoffDevices.objects.all())
    return JsonResponse(list_devices, safe=False)


def main_view(request):
    return render(request, 'device_vue/main_vue_app.html', {})
