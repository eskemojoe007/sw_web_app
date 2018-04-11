# Generated by Django 2.0.4 on 2018-04-11 00:56

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
                ('lattitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('sw_airport', models.BooleanField(verbose_name='Southwest Airport')),
                ('country', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
            ],
        ),
    ]
