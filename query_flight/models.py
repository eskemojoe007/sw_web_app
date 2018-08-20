from django.db import models
from timezone_field import TimeZoneField
from geopy.geocoders import Nominatim
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import numpy as np
from django.utils import timezone
import pytz
from six import string_types
import numpy as np


class AirportManager(models.Manager):
    def create(self, **kwargs):
        airport = self.lookup_missing(**kwargs)
        # airport = Airport(**kwargs)
        # airport.add_loc_fields()
        airport.save()
        return airport

    def lookup_missing(self, **kwargs):
        airport = Airport(**kwargs)
        airport.add_loc_fields()
        return airport


class Airport(models.Model):

    title = models.CharField(
        verbose_name='Long Name of Airport', max_length=50)
    timezone = TimeZoneField(default='US/Eastern')
    abrev = models.CharField(
        verbose_name='Airport Abreviation Code',
        max_length=4,
        primary_key=True)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)])
    sw_airport = models.BooleanField(verbose_name='Southwest Airport')

    country = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=20, blank=True)

    objects = AirportManager()

    sw_airport.admin_order_field = 'title'

    def __str__(self):
        # Return the title and abrev as the default string
        return self.title + " - " + self.abrev

    def _get_sub_loc(self, key):
        # Here we use geolocator to get the proper key
        geolocator = Nominatim()
        location = geolocator.reverse("{:f}, {:f}".format(
            self.latitude, self.longitude), timeout=10)

        # Lots and lots of error checking...looking for error from Geolocator
        # and for missing fields for international or other addresses

        if 'error' in location.raw:
            # Got an error back from geolocator
            raise ValidationError(_(
                "Geolocator error: %(error)s - Check you have the right Lat/Long or that you have connection"),
                params=location.raw, code='geolocator')

        # Got a response...but we may be missing keys...looking here
        try:
            return location.raw['address'][key]
        except KeyError as err:
            if err == 'address':
                raise ValidationError(
                    _('Got a response from Geolocator, but had no address'), code='no_address')
            elif err == key:
                raise ValidationError(_(
                    'Got a response from Geolocator, had an address, but didnt have key: %(key)s'),
                    params={
                    'key': err}, code='no_{}'.format(err))
            else:
                raise ValidationError(_(
                    'Got a response from Geolocator, had an address,KEY_ERROR of some kind %(raw)s'),
                    params={
                    'raw': location.raw}, code='some_key')
        except:
            raise ValidationError(
                _('Geolocator - NO CLUE WHAT WENT WRONG'), code='no_clue')

    def get_tz_obj(self):
        if isinstance(self.timezone, string_types):
            return pytz.timezone(self.timezone)
        else:
            return self.timezone

    def get_country_code(self):
        return self._get_sub_loc('country_code')

    def get_state(self):
        return self._get_sub_loc('state')

    def add_loc_fields(self):
        if (self.country is None) or (self.country == ''):
            self.country = self.get_country_code()
        if ((self.state is None) or (self.state == '')) and self.country == 'us':
            self.state = self.get_state()


class Search(models.Model):
    time = models.DateTimeField(auto_now=True)
    # TODO: Add user information here...

    def __str__(self):
        return '{} - {}'.format(self.id, self.time)

    def num_cards(self):
        return len(self.searchcard_set.all())

    def num_flights(self):
        n_f = 0
        for card in self.searchcard_set.all():
            n_f += card.num_flights()
        return n_f


class SearchCardManager(models.Manager):
    def create(self, search=None, **kwargs):

        # Create the search if it doesn't exist
        if search is None:
            search = Search.objects.create()

        # Create and save
        sc = SearchCard(search=search, **kwargs)
        sc.save()
        return sc


class SearchCard(models.Model):
    search = models.ForeignKey(
        Search, on_delete=models.CASCADE, verbose_name='Search')

    objects = SearchCardManager()

    def num_flights(self):
        n_f = 0
        for case in self.searchcase_set.all():
            n_f += case.num_flights()
        return n_f

    def origins(self):
        return np.unique(self.searchcase_set.values_list('origin_airport',flat=True))

    def destinations(self):
        return np.unique(self.searchcase_set.values_list('destination_airport', flat=True))

    # TODO: Add Dates here as well.

    def num_case(self):
        return self.searchcase_set.count()


class SearchCaseManager(models.Manager):
    def create(self, search_card=None, **kwargs):

        # Create the search Card if it doesn't exist
        if search_card is None:
            if 'search' in kwargs:
                search_card = SearchCard.objects.create(search=kwargs['search'])
            else:
                search_card = SearchCard.objects.create()

        # Make sure we remove search from any keys for kwargs...
        kwargs.pop('search', None)

        sc = self.validate_search_case(search_card=search_card, **kwargs)
        sc.save()
        return sc

    def validate_search_case(self, **kwargs):
        sc = SearchCase(**kwargs)
        if sc.origin_airport == sc.destination_airport:
            raise ValidationError(_(
                'Origin and Destination cant be the same: %(a)s'),
                params={'a': sc.origin_airport.abrev}, code='same_airports')
        return sc


class SearchCase(models.Model):
    search_card = models.ForeignKey(
        SearchCard, on_delete=models.CASCADE, verbose_name='Search Card')

    origin_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name='origin_case_set', verbose_name='Origin Airport')
    destination_airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name='destination_case_set', verbose_name='Destination Airport')
    date = models.DateField()

    # Set the custom Manager
    objects = SearchCaseManager()

    def num_flights(self):
        return self.flight_set.count()


class FlightManager(models.Manager):
    def create(self, **kwargs):
        flight = self.validate_flight(**kwargs)
        flight.save()
        return flight

    def validate_flight(self, **kwargs):
        flight = Flight(**kwargs)
        if flight.arrive_time < flight.depart_time:
            raise ValidationError(_(
                'Must depart before arriving. Depart: %(d)s, Arrive: %(a)s '),
                params={'a': flight.arrive_time, 'd': flight.depart_time}, code='badtimes')

        return flight


class Flight(models.Model):

    # TODO: Need to add point support...but for now just dollars.
    depart_time = models.DateTimeField(verbose_name='Departure Time')
    arrive_time = models.DateTimeField(verbose_name='Arrival Time')
    wanna_get_away = models.FloatField(
        validators=[MinValueValidator(0)], null=True, blank=True)
    anytime = models.FloatField(
        validators=[MinValueValidator(0)], null=True, blank=True)
    business_select = models.FloatField(
        validators=[MinValueValidator(0)], null=True, blank=True)
    search_case = models.ForeignKey(
        SearchCase, on_delete=models.CASCADE, verbose_name='SearchCase')

    objects = FlightManager()

    def __str__(self):
        # Return the title and abrev as the default string
        return '{} - {} - {}'.format(self.id, self.origin_airport().abrev, self.destination_airport().abrev)

    def travel_time(self):
        return self.arrive_time - self.depart_time

    def min_price(self):
        prices = [x for x in [self.wanna_get_away, self.anytime,
                              self.business_select] if (x is not None)]
        if len(prices) > 0:
            return np.min(prices)
        else:
            return None

    def num_layovers(self):
        return self.layover_set.count()

    def origin_airport(self):
        return self.search_case.origin_airport

    def destination_airport(self):
        return self.search_case.destination_airport


class LayoverManager(models.Manager):
    def create(self, **kwargs):
        self.validate_layover(**kwargs)
        layover = Layover(**kwargs)
        layover.save()
        return layover

    def validate_layover(self, **kwargs):
        # layover = Layover(**kwargs)
        if (kwargs['airport'] == kwargs['flight'].origin_airport) or(
                kwargs['airport'] == kwargs['flight'].destination_airport):

            raise ValidationError(_(
                'Layover (%(layover)s) cant happen at origin (%(origin)s) '
                'or destination (%(destination)s) '),
                params={'layover': kwargs['airport'],
                        'origin': kwargs['flight'].origin_airport,
                        'destination': kwargs['flight'].destination_airport},
                code='bad_layover')


class Layover(models.Model):
    airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, verbose_name='Airport')
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, verbose_name='Flight')
    change_planes = models.BooleanField(verbose_name='Change Planes?')
    time = models.FloatField(validators=[MinValueValidator(
        0)], verbose_name='Time of layover in seconds')

    objects = LayoverManager()

    def __str__(self):
        return '{} - {}'.format(self.airport.abrev, self.timedelta())

    def timedelta(self):
        return timezone.timedelta(seconds=self.time)

    # def clean(self):
    #     super().clean()
    #
    #     if (self.airport == self.flight.origin_airport) or(
    #         self.airport == self.flight.destination_airport):
    #
    #         raise ValidationError(_(
    #             'Layover ({layover}) cant happen at origin ({orign}) '
    #             'or destination ({destination}) '),
    #             params={'layover':self.airport,
    #                 'origin':self.flight.origin_airport,
    #                 'destination':self.flight.destination_airport},
    #             code='bad_layover')
