from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Airport,Flight,Layover
from django.utils import timezone
import pytest

# Helper functions that get and create airports
def create_atl(title='Atlanta',abrev='ATL',sw_airport=True,latitude=33.6407,
    longitude=-84.4277,timezone = 'US/Eastern'):
    return Airport.objects.create(title=title,abrev=abrev,sw_airport=sw_airport,
        latitude=latitude,longitude=longitude,timezone=timezone)

def get_atl(title='Atlanta',abrev='ATL',sw_airport=True,latitude=33.6407,
    longitude=-84.4277,timezone = 'US/Eastern',country=None,state=None):
    return Airport(title=title,abrev=abrev,sw_airport=sw_airport,
        latitude=latitude,longitude=longitude,timezone=timezone,country=country,state=state)

@pytest.fixture(scope='function',params=[str,timezone.pytz.timezone])
def tz_func(request):
    return request.param

@pytest.mark.django_db
class Test_Airport_Model(object):

    @pytest.mark.parametrize("lat,long,country,state",[
        (33.6407,-84.4277,'us','Georgia'),
        (51.1215,-114.0076,'ca','Alberta'),
        (9.9981,-84.2041,'cr','Provincia Alajuela'),
        (12.501400,-70.015198,'nl',''),
    ])
    def test_geo_lookup(self,lat,long,country,state):

        # Test the get functions
        airport = Airport(latitude=lat,longitude=long)
        assert airport.get_country_code() == country
        if state:
            assert airport.get_state() == state

        # Save and test the get and save
        airport = create_atl(latitude=lat,longitude=long)
        assert airport.country == country
        if country == 'us':
            assert airport.state == state
        else:
            assert airport.state == ''

    @pytest.mark.parametrize("kwargs,func",[
        ({'latitude':92.6407},'full_clean'),
        ({'latitude':92.6407},'save'),
        ({'latitude':92.6407,'country':'us','state':'GA'},'full_clean'),
        # ({'latitude':92.6407,'country':'us','state':'GA'},'save'),
        ({'latitude':-92.6407},'full_clean'),
        ({'longitude':-184.4277},'save'),
        ({'longitude':184.4277},'save'),
        ({'latitude':89.99},'full_clean'),
        ({'latitude':89.99},'save'),
        ({'timezone':'US/BlahBlah'},'full_clean'),
        ({'timezone':'US/BlahBlah'},'save'),

    ])
    def test_validators(self,kwargs,func):
        airport = get_atl(**kwargs)

        #Only testing the validators...not the save
        with pytest.raises(ValidationError)  as excinfo:
            f = getattr(airport,func)
            f()


    @pytest.mark.parametrize("tz",['US/Eastern','US/Mountain'])
    def test_timezone_codes(self,tz,tz_func):
        airport = create_atl(timezone=tz_func(tz))
        assert airport.get_tz_obj().zone == tz
        assert airport.get_tz_obj() == timezone.pytz.timezone(tz)


def get_flight():
    a = create_atl()
    b = create_atl(title='Boise',abrev='BOI',sw_airport=True,latitude=43.5658,
        longitude=-116.2223,timezone = 'US/Mountain')
    return Flight(origin_airport=a,destination_airport=b,
        depart_time=a.get_tz_obj().localize(timezone.datetime(2018,4,26,6,00,00)),
        arrive_time=b.get_tz_obj().localize(timezone.datetime(2018,4,26,13,50,00)),
        wanna_get_away=438.0,anytime=571.0,business_select=599.0)



class FlightModelTests(TestCase):
    def test_time_delta(self):
        # f = Flight(depart_time=pd.to_datetime('4/22/18 5:00 PM'),arrive_time=pd.to_datetime('4/22/18 10:00 PM'))
        f = Flight(depart_time=timezone.datetime(2018,4,22,17,00,00),arrive_time=timezone.datetime(2018,4,22,22,00,00))
        self.assertEqual(f.travel_time(),timezone.timedelta(hours=5))

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
        a = create_atl()
        f = Flight(origin_airport=a)
        self.assertIs(f.origin_airport.country,a.country)

    def test_tz_aware(self):
        '''
        Test the tz_aware of everything...so here we will build a real Flight
        Then test the timezone of everything.
        '''
        f = get_flight()
        f.save()

        self.assertTrue(timezone.is_aware(f.depart_time))
        self.assertTrue(timezone.is_aware(f.arrive_time))
        # self.assertIs(f.arrive_time.is_aware(),True)

    def test_timedelta_timezone(self):
        f = get_flight()
        self.assertEqual(f.travel_time(),timezone.timedelta(hours=9,minutes=50))
    def test_timedelta_timezone_save(self):
        f = get_flight()
        f.save()
        self.assertEqual(f.travel_time(),timezone.timedelta(hours=9,minutes=50))

class LayoverModelTests(TestCase):
    def test_str(self):
        a = create_atl()
        l = Layover(airport=a,time=20)

        self.assertEqual(l.__str__(),'{} - {}'.format(a.abrev,l.get_timedelta()))

    def test_min_time(self):
        f = get_flight()
        a = f.origin_airport

        layover = Layover(airport=a,flight=f,change_planes=True,time=-10)
        with self.assertRaises(ValidationError):
            layover.full_clean()



    # def test_tz_specifics(self):
    #     '''
    #     Test the tz_aware of everything...so here we will build a real Flight
    #     Then test the timezone of everything.
    #     '''
    #     a = create_atl()
    #     b = create_atl(title='Boise',abrev='BOI',sw_airport=True,latitude=43.5658,
    #         longitude=-116.2223,timezone = 'US/Mountain')
    #
    #     f = Flight(origin_airport=a,destination_airport=b,
    #         depart_time=pd.to_datetime('2018-04-26 6:00 AM'),
    #         arrive_time=pd.to_datetime('2018-04-26 1:50 PM'),
    #         wanna_get_away=438.0,anytime=571.0,business_select=599.0)
    #
    #     f.save()
    #
    #     self.assertIs(f.depart_time.is_aware(),True)
    #     self.assertIs(f.arrive_time.is_aware(),True)
