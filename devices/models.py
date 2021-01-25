from django.db import models


# Create your models here.
class SonoffDevices(models.Model):
    class Meta:
        verbose_name = "Устройства"

    NORMAL = 0
    MIN_WARN = 1
    MAX_WARN = 2
    MIN_ALARM = 3
    MAX_ALARM = 4

    STATUSES = [
        (NORMAL, 'Норма'),
        (MIN_WARN, 'Предупреждение: значение ниже нормы'),
        (MAX_WARN, 'Предупреждение: значение выше нормы'),
        (MIN_ALARM, 'Тревога: значение ниже нормы'),
        (MAX_ALARM, 'Тревога: значение выше нормы'),
    ]

    name = models.CharField(max_length=100, null=False, blank=False, db_index=True, verbose_name='Название устройсва')
    device_id = models.CharField(max_length=12, null=False, blank=False, db_index=True, verbose_name='Идентификатор')
    model = models.CharField(max_length=20, null=True, blank=True, verbose_name='Модель устройства')
    mac = models.CharField(max_length=20, null=True, blank=True, verbose_name='MAC адресс')
    sensor_type = models.CharField(max_length=20, null=True, blank=True, verbose_name='Тип сенсора')
    firmware = models.CharField(max_length=10, null=True, blank=True, verbose_name='Версия прошивки')
    is_online = models.BooleanField(default=False, blank=True, verbose_name='Усройство онлайн')
    signal = models.FloatField(null=True, default=None, blank=True, verbose_name='Качество WIFI сигнала')
    last_temperature = models.FloatField(null=True, default=None, blank=True,
                                         verbose_name='Последняя зарегистрированная температура')
    last_humidity = models.FloatField(null=True, default=None, blank=True,
                                      verbose_name='Последняя зарегистрированная влажность')
    switch = models.BooleanField(default=False, blank=True, verbose_name='Реле активировано')
    date_of_modify = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    last_on_line = models.DateTimeField(null=True, default=None, blank=True,
                                        verbose_name='Время последнего появления в сети')
    last_off_line = models.DateTimeField(null=True, default=None, blank=True,
                                         verbose_name='Время последнего пропадания из сети')
    temperature_minimal_warning_value = models.FloatField(null=True, default=None, blank=True,
                                                          verbose_name='Нижний порог срабатывания предуприждения по температуре')
    temperature_maximal_warning_value = models.FloatField(null=True, default=None, blank=True,
                                                          verbose_name='Верхний порог срабатывания предуприждения  по температуре')
    temperature_minimal_alarm_value = models.FloatField(null=True, default=None, blank=True,
                                                        verbose_name='Нижний порог срабатывания тревоги по температуре')
    temperature_maximal_alarm_value = models.FloatField(null=True, default=None, blank=True,
                                                        verbose_name='Верхний порог срабатывания тревоги по температуре')
    temperature_status = models.IntegerField(default=NORMAL, choices=STATUSES, verbose_name='состояние по температуре')
    temperature_histeresis_value = models.FloatField(null=True, default=None, blank=True,
                                                     verbose_name='Значение гистерезиса по температуре')
    humidity_minimal_warning_value = models.FloatField(null=True, default=None, blank=True,
                                                       verbose_name='Нижний порог срабатывания предуприждения по влажности')
    humidity_maximal_warning_value = models.FloatField(null=True, default=None, blank=True,
                                                       verbose_name='Верхний порог срабатывания предуприждения по влажности')
    humidity_minimal_alarm_value = models.FloatField(null=True, default=None, blank=True,
                                                     verbose_name='Нижний порог срабатывания тревоги по влажности')
    humidity_maximal_alarm_value = models.FloatField(null=True, default=None, blank=True,
                                                     verbose_name='Верхний порог срабатывания тревоги по влажности')
    humidity_status = models.IntegerField(default=NORMAL, choices=STATUSES, verbose_name='состояние по влажности')
    humidity_histeresis_value = models.FloatField(null=True, default=None, blank=True,
                                                  verbose_name='Значение гистерезиса по влажности')

    def set_humidity_value(self, value):
        status = self.NORMAL
        if self.humidity_minimal_alarm_value is not None:
            if value <= self.humidity_minimal_alarm_value:
                status = self.MIN_ALARM
            elif self.humidity_status == self.MIN_ALARM \
                    and value >= self.humidity_minimal_alarm_value + self.humidity_histeresis_value:
                status = self.NORMAL

        if self.humidity_minimal_warning_value is not None:
            if value <= self.humidity_minimal_warning_value and status == self.NORMAL:
                status = self.MIN_WARN
            elif self.humidity_status == self.MIN_WARN \
                    and value >= self.humidity_minimal_warning_value + self.humidity_histeresis_value:
                status = self.NORMAL

        if self.humidity_maximal_warning_value is not None:
            if value >= self.humidity_maximal_warning_value and status == self.NORMAL:
                status = self.MAX_WARN
            elif self.humidity_status == self.MAX_WARN \
                    and value <= self.humidity_maximal_warning_value - self.humidity_histeresis_value:
                status = self.NORMAL

        if self.humidity_maximal_alarm_value is not None:
            if value >= self.humidity_maximal_alarm_value:
                status = self.MAX_ALARM
            elif self.humidity_status == self.MAX_ALARM \
                    and value <= self.humidity_maximal_alarm_value - self.humidity_histeresis_value:
                status = self.NORMAL

        self.humidity_status = status
        self.last_humidity = value

    def set_temperature_value(self, value):
        status = self.NORMAL
        if self.temperature_minimal_alarm_value is not None:
            if value <= self.temperature_minimal_alarm_value:
                status = self.MIN_ALARM
            elif self.temperature_status == self.MIN_ALARM \
                    and value >= self.temperature_minimal_alarm_value + self.temperature_histeresis_value:
                status = self.NORMAL

        if self.temperature_minimal_warning_value is not None:
            if value <= self.temperature_minimal_warning_value and status == self.NORMAL:
                status = self.MIN_WARN
            elif self.temperature_status == self.MIN_WARN \
                    and value >= self.temperature_minimal_warning_value + self.temperature_histeresis_value:
                status = self.NORMAL

        if self.temperature_maximal_warning_value is not None:
            if value >= self.temperature_maximal_warning_value and status == self.NORMAL:
                status = self.MAX_WARN
            elif self.temperature_status == self.MAX_WARN \
                    and value <= self.temperature_maximal_warning_value - self.temperature_histeresis_value:
                status = self.NORMAL

        if self.temperature_maximal_alarm_value is not None:
            if value >= self.temperature_maximal_alarm_value:
                status = self.MAX_ALARM
            elif self.temperature_status == self.MAX_ALARM \
                    and value <= self.temperature_maximal_alarm_value - self.temperature_histeresis_value:
                status = self.NORMAL

        self.temperature_status = status
        self.last_temperature = value

    def __str__(self):
        return "{} ({})".format(self.name, self.device_id)


class SonoffDevicesValues(models.Model):
    class Meta:
        verbose_name = "Архив значений данных от устройств"

    temperature = models.FloatField(null=True, default=None, blank=True, verbose_name='Температура')
    humidity = models.FloatField(null=True, default=None, blank=True, verbose_name='Влажность')
    switch = models.BooleanField(default=False, blank=True, verbose_name='Реле активировано')
    date_of_modify = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    temperature_status = models.IntegerField(default=SonoffDevices.NORMAL, choices=SonoffDevices.STATUSES,
                                             verbose_name='состояние по температуре')
    humidity_status = models.IntegerField(default=SonoffDevices.NORMAL, choices=SonoffDevices.STATUSES,
                                          verbose_name='состояние по влажности')
    signal = models.FloatField(null=True, default=None, blank=True, verbose_name='Качество WIFI сигнала')
    device = models.ForeignKey(SonoffDevices, on_delete=models.CASCADE, verbose_name='Устройство',
                               related_name='values')


class DeviceGroups(models.Model):
    class Meta:
        verbose_name = "Группы устройств"

    name = models.CharField(max_length=100, null=False, blank=False, db_index=True, verbose_name='Название группы')
    devices = models.ManyToManyField(SonoffDevices)

    def __str__(self):
        return "{}".format(self.name)


class TelegramUsers(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, db_index=True, verbose_name='Имя пользователя')
    humidity_notify = models.BooleanField(default=False, blank=True,
                                          verbose_name='Извещать об превышениях по влажности')
    temperature_notify = models.BooleanField(default=False, blank=True,
                                             verbose_name='Извещать об превышениях по температуре')
    offline_notify = models.BooleanField(default=False, blank=True, verbose_name='Извещать об пропавших устройствах')

    class Meta:
        verbose_name = "Пользователи Telegram для оповещений"


class DeviceTelegramUsers(models.Model):
    device = models.ForeignKey(SonoffDevices, on_delete=models.CASCADE, verbose_name='Устройство',
                               related_name='notify_users')
    telegram_users = models.ForeignKey(TelegramUsers, on_delete=models.CASCADE,
                                       verbose_name='Пользователь для извещения')
    humidity_notify = models.BooleanField(default=False, blank=True,
                                          verbose_name='Извещать об превышениях по влажности')
    temperature_notify = models.BooleanField(default=False, blank=True,
                                             verbose_name='Извещать об превышениях по температуре')
    offline_notify = models.BooleanField(default=False, blank=True, verbose_name='Извещать об пропавших устройствах')

    class Meta:
        verbose_name = "Telegram для оповещение по устройствам"
