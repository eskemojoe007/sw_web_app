# Generated by Django 2.1 on 2018-08-28 00:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('query_flight', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='search',
            name='time',
        ),
        migrations.AddField(
            model_name='search',
            name='completed',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='search',
            name='started',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='search',
            name='submitted',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]