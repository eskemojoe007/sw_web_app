from django.db import models
from timezone_field import TimeZoneField
import reverse_geocoder as rg


class Airport(models.Model):
    title = models.CharField(verbose_name='Long Name of Airport',max_length=50)
    timezone = TimeZoneField(default='US/Eastern')
    abrev = models.CharField(verbose_name='Airport Abreviation Code',max_length=4,primary_key=True)
    lattitude = models.FloatField()
    longitude = models.FloatField()
    sw_airport = models.BooleanField(verbose_name='Southwest Airport')

    sw_airport.admin_order_field = 'title'

    def __str__(self):
        return self.title + " - " + self.abrev

    def get_state(self):
        return rg.search((self.lattitude,self.longitude))[0]['admin1']

    def get_country(self):
        return rg.search((self.lattitude,self.longitude))[0]['cc']

    get_state.short_description = 'State'
