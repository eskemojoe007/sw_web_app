# Generated by Django 2.0.5 on 2018-06-03 17:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query_flight', '0006_auto_20180519_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='arrive_time',
            field=models.DateTimeField(verbose_name='Arrival Time'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='depart_time',
            field=models.DateTimeField(verbose_name='Departure Time'),
        ),
        migrations.AlterField(
            model_name='layover',
            name='time',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Time of layover in seconds'),
        ),
    ]
