from django.db import models
from timezone_field import TimeZoneField
from geopy.geocoders import Nominatim

class Airport(models.Model):

    def get_sub_loc(self,key):
        geolocator = Nominatim()
        location = geolocator.reverse("{:f}, {:f}".format(self.lattitude,self.longitude))
        return location.raw['address'][key]

    def get_country_code(self):
        return self.get_sub_loc('country_code')

    def get_state(self):
        return self.get_sub_loc('state')

    title = models.CharField(verbose_name='Long Name of Airport',max_length=50)
    timezone = TimeZoneField(default='US/Eastern')
    abrev = models.CharField(verbose_name='Airport Abreviation Code',max_length=4,primary_key=True)
    lattitude = models.FloatField()
    longitude = models.FloatField()
    sw_airport = models.BooleanField(verbose_name='Southwest Airport')

    # country = models.CharField(max_length=20,blank=True,default=get_country_code)
    # state = models.CharField(max_length=20,blank=True,default=get_state)
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=20)

    sw_airport.admin_order_field = 'title'

    def __str__(self):
        return self.title + " - " + self.abrev

    def save(self, *args, **kwargs):
        if (self.country is None) or (self.country == ''):
            self.country = self.get_country_code()
        if (self.state is None) or (self.state == ''):
            self.state = self.get_state()

        super().save(*args,**kwargs)
