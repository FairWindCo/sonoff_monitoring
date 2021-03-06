# Generated by Django 3.0.2 on 2021-01-18 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0007_auto_20210118_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicetelegramusers',
            name='humidity_notify',
            field=models.BooleanField(blank=True, default=False, verbose_name='Извещать об превышениях по влажности'),
        ),
        migrations.AddField(
            model_name='devicetelegramusers',
            name='offline_notify',
            field=models.BooleanField(blank=True, default=False, verbose_name='Извещать об пропавших устройствах'),
        ),
        migrations.AddField(
            model_name='devicetelegramusers',
            name='temperature_notify',
            field=models.BooleanField(blank=True, default=False, verbose_name='Извещать об превышениях по температуре'),
        ),
    ]
