from django.contrib import admin

# Register your models here.
from devices.models import SonoffDevices, DeviceGroups


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_id', 'is_online', 'last_on_line', 'date_of_modify')
    search_fields = ('name', 'device_id', 'last_on_line', )
    readonly_fields = ['device_id',
                       'mac',
                       'is_online',
                       'sensor_type',
                       'model',
                       'firmware',
                       'signal',
                       'switch',
                       'date_of_modify',
                       'last_on_line',
                       'last_off_line']

class GroupAdmin(admin.ModelAdmin):
    pass

admin.site.register(SonoffDevices, DeviceAdmin)
admin.site.register(DeviceGroups, GroupAdmin)