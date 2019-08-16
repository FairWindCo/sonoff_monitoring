from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from devices.models import SonoffDevices, SonoffDevicesValues
import time
import datetime


class Command(BaseCommand):
    help = 'Refresh device info'

    def handle(self, *args, **options):
        from sonoff import sonoff
        devices = []
        try:
            s = sonoff.Sonoff('sergey.manenok@gmail.com', 'q1s2c3f4t5', 'eu')
            s.update_devices()
            devices = s.get_devices()
        except Exception as e:
            raise CommandError(e)
        SonoffDevices.objects.all().update(is_online=False)

        #print(timezone.get_current_timezone())
        #print(timezone.get_default_timezone())
        for device in devices:
            # We found a device, lets turn something on
            #print(device)
            device_id = device['deviceid']
            value = None
            db_device = SonoffDevices.objects.filter(**{'device_id': device_id})

            if not db_device:
                db_device = SonoffDevices()
                db_device.name = device['name']
                db_device.device_id = device_id
                db_device.model = device['brandName']+' '+device['productModel']
                db_device.mac = device['params']['staMac']
                db_device.sensor_type = device['params']['sensorType']
                db_device.firmware = device['params']['fwVersion']
                db_device.signal = device['params']['rssi']
            else:
                db_device = db_device[0]
            if device['online']:
                db_device.signal = float(device['params']['rssi'])
                if 'currentTemperature' in device['params'] and device['params']['currentTemperature'] != 'unavailable':
                    db_device.set_temperature_value(float(device['params']['currentTemperature']))
                if 'currentHumidity' in device['params'] and device['params']['currentHumidity'] != 'unavailable':
                    db_device.set_humidity_value(float(device['params']['currentHumidity']))
                if 'switch' in device['params']:
                    db_device.switch = True if device['params']['switch'] == 'on' else False

                db_device.save()
                value = SonoffDevicesValues()
                value.temperature = db_device.last_temperature
                value.humidity = db_device.last_humidity
                value.switch = db_device.switch
                value.device = db_device
                value.humidity_status = db_device.humidity_status
                value.temperature_status = db_device.temperature_status
                value.signal = db_device.signal

            db_device.is_online = device['online']

            db_device.last_on_line = timezone.datetime.strptime(device['onlineTime'], '%Y-%m-%dT%H:%M:%S.%f%z')#.astimezone(timezone.get_current_timezone())
            db_device.last_off_line = timezone.datetime.strptime(device['offlineTime'],
                                                                '%Y-%m-%dT%H:%M:%S.%f%z')  # .astimezone(timezone.get_current_timezone())
            db_device.save()
            if value:
                value.save()
            #print(timezone.datetime.strptime(device['onlineTime'], '%Y-%m-%dT%H:%M:%S.%f%z'))
            #print(timezone.datetime.strptime(device['onlineTime'], '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(timezone.get_current_timezone()))
            self.stdout.write(self.style.SUCCESS('Read device info "%s"' % (device_id,)))
        self.stdout.write(self.style.SUCCESS('Device info refreshed'))