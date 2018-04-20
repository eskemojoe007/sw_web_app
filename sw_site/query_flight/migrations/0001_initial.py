# Generated by Django 2.0.4 on 2018-04-20 15:50

import django.core.validators
from django.db import migrations, models
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('title', models.CharField(max_length=50, verbose_name='Long Name of Airport')),
                ('timezone', timezone_field.fields.TimeZoneField(default='US/Eastern')),
                ('abrev', models.CharField(max_length=4, primary_key=True, serialize=False, verbose_name='Airport Abreviation Code')),
                ('lattitude', models.FloatField(validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('longitude', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('sw_airport', models.BooleanField(verbose_name='Southwest Airport')),
                ('country', models.CharField(blank=True, max_length=20)),
                ('state', models.CharField(blank=True, max_length=20)),
            ],
        ),
    ]
