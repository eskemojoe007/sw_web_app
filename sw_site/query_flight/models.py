from django.db import models
from timezone_field import TimeZoneField
from geopy.geocoders import Nominatim
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class Airport(models.Model):

    title = models.CharField(verbose_name='Long Name of Airport',max_length=50)
    timezone = TimeZoneField(default='US/Eastern')
    abrev = models.CharField(verbose_name='Airport Abreviation Code',max_length=4,primary_key=True)
    lattitude = models.FloatField(validators=[MinValueValidator(-90),MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180),MaxValueValidator(180)])
    sw_airport = models.BooleanField(verbose_name='Southwest Airport')

    country = models.CharField(max_length=20,blank=True)
    state = models.CharField(max_length=20,blank=True)

    sw_airport.admin_order_field = 'title'



    def __str__(self):
        # Return the title and abrev as the default string
        return self.title + " - " + self.abrev


    def _get_sub_loc(self,key):
        # Here we use geolocator to get the proper key
        geolocator = Nominatim()
        location = geolocator.reverse("{:f}, {:f}".format(self.lattitude,self.longitude))

        # Lots and lots of error checking...looking for error from Geolocator
        # and for missing fields for international or other addresses

        if 'error' in location.raw:
            # Got an error back from geolocator
            raise ValidationError(_(
                "Geolocator error: %(error)s - Check you have the right Lat/Long or that you have connection"),
                params=location.raw,code='geolocator')

        # Got a response...but we may be missing keys...looking here
        try:
            return location.raw['address'][key]
        except KeyError as err:
            if err == 'address':
                raise ValidationError(_('Got a response from Geolocator, but had no address'),code='no_address')
            elif err == key:
                raise ValidationError(_('Got a response from Geolocator, had an address, but didnt have key: %(key)s'),params={'key':err},code='no_{}'.format(err))
            else:
                raise ValidationError(_('Got a response from Geolocator, had an address,KEY_ERROR of some kind'),code='some_key')
        except:
            raise ValidationError(_('NO CLUE WHAT WENT WRONG'),code='no_clue')

    def get_country_code(self):
        return self._get_sub_loc('country_code')

    def get_state(self):
        return self._get_sub_loc('state')

    def add_loc_fields(self):
        if (self.country is None) or (self.country == ''):
            self.country = self.get_country_code()
        if (self.state is None) or (self.state == ''):
            self.state = self.get_state()

    def save(self, *args, **kwargs):
        # Overright save so we can look up the coutnry and state if its missing
        # as it is optional.  If its empty or none...go look it up
        self.add_loc_fields()
        super().save(*args,**kwargs)

    def clean(self):
        # Overwrite clean so we can add the fields and validate properly if they are missing.
        super().clean()
        self.add_loc_fields()
