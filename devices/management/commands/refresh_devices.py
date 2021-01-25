from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from devices.models import SonoffDevices, SonoffDevicesValues, TelegramUsers
from telegrams.telegram_message import run_send_message_to_clients


class Command(BaseCommand):
    help = 'Refresh device info'

    def handle(self, *args, **options):
        from sonoff import sonoff
        devices = []
        try:
            s = sonoff.Sonoff(settings.SONOFF_USER, settings.SONOFF_PASS, 'eu')
            s.update_devices()
            devices = s.get_devices()
        except Exception as e:
            raise CommandError(e)
        SonoffDevices.objects.all().update(is_online=False)

        # print(timezone.get_current_timezone())
        # print(timezone.get_default_timezone())
        humidity_notify = ''
        temperature_notify = ''
        offline_notify = ''

        humidity_notify_users = set()
        temperature_notify_users = set()
        offline_notify_users = set()

        for device in devices:
            message = ''
            # We found a device, lets turn something on
            print(device)
            device_id = device['deviceid']
            value = None
            db_device = SonoffDevices.objects.filter(**{'device_id': device_id})

            if not db_device:
                db_device = SonoffDevices()
                db_device.name = device['name']
                db_device.device_id = device_id
                db_device.model = device['brandName'] + ' ' + device['productModel']
                db_device.mac = device['params']['staMac']
                db_device.sensor_type = device['params']['sensorType']
                db_device.firmware = device['params']['fwVersion']
                db_device.signal = device['params']['rssi']
            else:
                db_device = db_device[0]
            if device['online']:
                db_device.signal = float(device['params']['rssi'])
                if 'currentTemperature' in device['params'] and device['params']['currentTemperature'] != 'unavailable':
                    old_status = db_device.temperature_status
                    db_device.set_temperature_value(float(device['params']['currentTemperature']))
                    if old_status != db_device.temperature_status:
                        temperature_notify += f'DEVICE: {db_device.name} ТЕМПЕРАТУРА: {db_device.last_temperature} ' \
                                              f'({SonoffDevices.STATUSES[db_device.temperature_status][1]}) \n'
                if 'currentHumidity' in device['params'] and device['params']['currentHumidity'] != 'unavailable':
                    old_status = db_device.humidity_status
                    db_device.set_humidity_value(float(device['params']['currentHumidity']))
                    if old_status != db_device.humidity_status:
                        humidity_notify += f'DEVICE: {db_device.name} ВЛАЖНОСТЬ: {db_device.last_humidity}' \
                                           f'{SonoffDevices.STATUSES[db_device.humidity_status][1]} \n'
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

            db_device.last_on_line = timezone.datetime.strptime(device['onlineTime'],
                                                                '%Y-%m-%dT%H:%M:%S.%f%z')  # .astimezone(timezone.get_current_timezone())
            db_device.last_off_line = timezone.datetime.strptime(device['offlineTime'],
                                                                 '%Y-%m-%dT%H:%M:%S.%f%z')  # .astimezone(timezone.get_current_timezone())

            if db_device.is_online and not device['online']:
                offline_notify += f'УСТРОЙСТВО: {db_device.name} НЕ В СЕТИ c {db_device.last_off_line}'

            db_device.is_online = device['online']

            db_device.save()

            if value:
                value.save()
            # print(timezone.datetime.strptime(device['onlineTime'], '%Y-%m-%dT%H:%M:%S.%f%z'))
            # print(timezone.datetime.strptime(device['onlineTime'], '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(timezone.get_current_timezone()))

            if any([humidity_notify, temperature_notify, offline_notify]):
                if humidity_notify:
                    user_list = [notify_users.telegram_users.name for notify_users in
                                 db_device.notify_users.filter(humidity_notify__exact=True).all()]
                    humidity_notify_users.update(user_list)
                if temperature_notify:
                    user_list = [notify_users.telegram_users.name for notify_users in
                                 db_device.notify_users.filter(temperature_notify__exact=True).all()]
                    temperature_notify_users.update(user_list)
                if offline_notify:
                    user_list = [notify_users.telegram_users.name for notify_users in
                                 db_device.notify_users.filter(offline_notify__exact=True).all()]
                    offline_notify_users.update(user_list)

            self.stdout.write(self.style.SUCCESS('Read device info "%s"' % (device_id,)))

        if humidity_notify or temperature_notify or offline_notify:
            if humidity_notify:
                user_list = [notify_users.name for notify_users in
                             TelegramUsers.objects.filter(humidity_notify__exact=True).all()]
                humidity_notify_users.update(user_list)
                run_send_message_to_clients(humidity_notify_users, humidity_notify, settings.TELEGRAM_API_ID,
                                            settings.TELEGRAM_HASH)
            if temperature_notify:
                user_list = [notify_users.name for notify_users in
                             TelegramUsers.objects.filter(temperature_notify__exact=True).all()]
                temperature_notify_users.update(user_list)
                run_send_message_to_clients(temperature_notify_users, temperature_notify, settings.TELEGRAM_API_ID,
                                            settings.TELEGRAM_HASH)
            if offline_notify:
                user_list = [notify_users.name for notify_users in
                             TelegramUsers.objects.filter(offline_notify__exact=True).all()]
                offline_notify_users.update(user_list)
                run_send_message_to_clients(offline_notify_users, offline_notify, settings.TELEGRAM_API_ID,
                                            settings.TELEGRAM_HASH)

        self.stdout.write(self.style.SUCCESS('Device info refreshed'))
