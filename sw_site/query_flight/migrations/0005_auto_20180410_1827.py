# Generated by Django 2.0.4 on 2018-04-10 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query_flight', '0004_airport_sw_airport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airport',
            name='lattitude',
            field=models.FloatField(max_length=25),
        ),
        migrations.AlterField(
            model_name='airport',
            name='longitude',
            field=models.FloatField(max_length=25),
        ),
    ]
