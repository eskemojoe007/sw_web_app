from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Airport,Flight
import pandas as pd
import pytz


# Create your tests here.

def create_atl(title='Atlanta',abrev='ATL',sw_airport=True,latitude=33.6407,
    longitude=-84.4277,timezone = 'US/Eastern'):
    return Airport.objects.create(title=title,abrev=abrev,sw_airport=sw_airport,
        latitude=latitude,longitude=longitude,timezone=timezone)

def get_atl(title='Atlanta',abrev='ATL',sw_airport=True,latitude=33.6407,
    longitude=-84.4277,timezone = 'US/Eastern'):
    return Airport(title=title,abrev=abrev,sw_airport=sw_airport,
        latitude=latitude,longitude=longitude,timezone=timezone)

class AirportModelTests(TestCase):
    def test_atl_lookup(self):
        # does it look up country and state for a common airport atl?
        atl = Airport(latitude=33.6407,longitude=-84.4277)
        self.assertEqual(atl.get_country_code(),'us')
        self.assertEqual(atl.get_state(),'Georgia')

    def test_foreign_lookup(self):
        #Testing calgary airport lookup
        yyc = Airport(latitude=51.1215,longitude=-114.0076)
        self.assertEqual(yyc.get_country_code(),'ca')
        self.assertEqual(yyc.get_state(),'Alberta')

        #Checking San Jose Costa Rica airport
        sjo = Airport(latitude=9.9981,longitude=-84.2041)
        self.assertEqual(sjo.get_country_code(),'cr')
        self.assertEqual(sjo.get_state(),'Provincia Alajuela')

        #Checking Aruba airport
        aua = Airport(latitude=12.501400,longitude=-70.015198)
        self.assertEqual(aua.get_country_code(),'nl')

    def test_lookup_save(self):
        # Actually saves a value, and sees if the save function is working properly
        atl = create_atl()

        self.assertEqual(atl.state,'Georgia')
        self.assertEqual(atl.country,'us')

    def test_lookup_save_international(self):
        # Actually saves a value, and sees if the save function is working properly
        aua = Airport.objects.create(title='Aruba',abrev='AUA',sw_airport=True,
            latitude=12.501400,longitude=-70.015198)

        self.assertEqual(aua.country,'nl')
        self.assertEqual(aua.state,'')

    def test_lat_validator(self):
        airport = get_atl(latitude=92.6407)

        #Only testing the validators...not the save
        with self.assertRaises(ValidationError):
            airport.full_clean()

    def test_long_validator(self):
        airport = get_atl(longitude=-184.4277)

        #Only testing the validators...not the save
        with self.assertRaises(ValidationError):
            airport.full_clean()

    def test_geolocator_error(self):
        airport = get_atl(latitude=89.99)

        #Only testing the validators...not the save
        with self.assertRaises(ValidationError):
            airport.full_clean()

    def test_geolocator_error_save(self):
        airport = get_atl(latitude=89.99)

        #Only testing the validators...not the save
        with self.assertRaises(ValidationError):
            airport.save()

    # TODO: Get this to work...thought it should make a tz obj...not just a string
    # need to get string to obj working.
    def test_timezone_codes(self):
        airport = create_atl(timezone=pytz.timezone('US/Eastern'))
        print(repr(airport.timezone))
        self.assertIs(airport.timezone,pytz.timezone('US/Eastern'))

    def test_timezone_bad_input(self):
        airport = get_atl(timezone='US/BlahBlah')
        with self.assertRaises(ValidationError):
            airport.full_clean()

class FlightModelTests(TestCase):
    def test_time_delta(self):
        f = Flight(depart_time=pd.to_datetime('4/22/18 5:00 PM'),arrive_time=pd.to_datetime('4/22/18 10:00 PM'))
        self.assertEqual(f.travel_time(),pd.to_timedelta('5:00:00'))

    def test_min_price_0(self):
        f = Flight(wanna_get_away=100.00)
        self.assertEqual(f.min_price(),100.00)

    def test_min_price_1(self):
        f = Flight(anytime=100.00)
        self.assertEqual(f.min_price(),100.00)

    def test_min_price_2(self):
        f = Flight(business_select=100.00)
        self.assertEqual(f.min_price(),100.00)

    def test_min_price_3(self):
        f = Flight(wanna_get_away= 100.00, business_select=150.00)
        self.assertEqual(f.min_price(),100.00)

    def test_min_price_4(self):
        f = Flight()
        self.assertIs(f.min_price(),None)

    def test_airport_connection(self):
        a = Airport.objects.create(title='Atlanta',abrev='ATL',sw_airport=True,
            latitude=33.6407,longitude=-84.4277)
        f = Flight(origin_airport=a)
        self.assertIs(f.origin_airport.country,a.country)
