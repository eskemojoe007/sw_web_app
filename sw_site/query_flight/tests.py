from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Airport


# Create your tests here.


class AirportModelTests(TestCase):
    def test_atl_lookup(self):
        # does it look up country and state for a common airport atl?
        atl = Airport(lattitude=33.6407,longitude=-84.4277)
        self.assertEqual(atl.get_country_code(),'us')
        self.assertEqual(atl.get_state(),'Georgia')

    def test_foreign_lookup(self):
        #Testing calgary airport lookup
        yyc = Airport(lattitude=51.1215,longitude=-114.0076)
        self.assertEqual(yyc.get_country_code(),'ca')
        self.assertEqual(yyc.get_state(),'Alberta')

        #Checking San Jose Costa Rica airport
        sjo = Airport(lattitude=9.9981,longitude=-84.2041)
        self.assertEqual(sjo.get_country_code(),'cr')
        self.assertEqual(sjo.get_state(),'Provincia Alajuela')

    def test_lookup_save(self):
        # Actually saves a value, and sees if the save function is working properly
        atl = Airport.objects.create(title='Atlanta',abrev='ATL',sw_airport=True,
            lattitude=33.6407,longitude=-84.4277)

        self.assertEqual(atl.state,'Georgia')
        self.assertEqual(atl.country,'us')

    def test_lat_validator(self):
        airport = Airport(title='Atlanta',abrev='ATL',sw_airport=True,
            lattitude=92.6407,longitude=-84.4277)

        #Only testing the validators...not the save
        with self.assertRaises(ValidationError):
            airport.full_clean()

    def test_long_validator(self):
        airport = Airport(title='Atlanta',abrev='ATL',sw_airport=True,
        lattitude=33.6407,longitude=-184.4277)

        #Only testing the validators...not the save
        with self.assertRaises(ValidationError):
            airport.full_clean()

    def test_geolocator_error(self):
        airport = Airport(title='Atlanta',abrev='ATL',sw_airport=True,
        lattitude=89.99,longitude=-84.4277)

        #Only testing the validators...not the save
        with self.assertRaises(ValidationError):
            airport.full_clean()

    def test_geolocator_error_save(self):
        airport = Airport(title='Atlanta',abrev='ATL',sw_airport=True,
        lattitude=89.99,longitude=-84.4277)

        #Only testing the validators...not the save
        with self.assertRaises(ValidationError):
            airport.save()
