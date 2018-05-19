from django.core.exceptions import ValidationError
from query_flight.models import Airport
from django.utils import timezone
import pytest

# Helper functions that get and create airports
def get_airport(**kwargs):
    return Airport(**kwargs)
def create_airport(**kwargs):
    return Airport.objects.create(**kwargs)

# def overwrite_dict(d,**kwargs):
#     for key, value in kwargs.items():
#         d.update({key,value})


# def create_atl(title='Atlanta',abrev='ATL',sw_airport=True,latitude=33.6407,
#     longitude=-84.4277,timezone = 'US/Eastern'):
#     return Airport.objects.create(title=title,abrev=abrev,sw_airport=sw_airport,
#         latitude=latitude,longitude=longitude,timezone=timezone)
#
# def get_atl(title='Atlanta',abrev='ATL',sw_airport=True,latitude=33.6407,
#     longitude=-84.4277,timezone = 'US/Eastern',country=None,state=None):
#     return Airport(title=title,abrev=abrev,sw_airport=sw_airport,
#         latitude=latitude,longitude=longitude,timezone=timezone,country=country,state=state)

# @pytest.fixture(scope='function',params=[str,timezone.pytz.timezone])
# def tz_func(request):
#     return request.param

@pytest.mark.django_db
class Test_Airport_Model(object):

    @pytest.mark.parametrize("lat,long,country,state",[
        (33.6407,-84.4277,'us','Georgia'),
        (51.1215,-114.0076,'ca','Alberta'),
        (9.9981,-84.2041,'cr','Provincia Alajuela'),
        (12.501400,-70.015198,'nl',''),
    ])
    def test_geo_lookup(self,lat,long,country,state,atl):

        # Test the get functions
        airport = Airport(latitude=lat,longitude=long)
        assert airport.get_country_code() == country
        if state:
            assert airport.get_state() == state

        # Save and test the get and save
        # airport_dict = overwrite_dict(atl,latitude=lat,longitude=long)
        atl.update({'latitude':lat,'longitude':long})
        airport = create_airport(**atl)
        assert airport.country == country
        if country == 'us':
            assert airport.state == state
        else:
            assert airport.state == ''

    @pytest.mark.parametrize("kwargs,func",[
        ({'latitude':92.6407},'full_clean'),
        ({'latitude':92.6407},'save'),
        ({'latitude':92.6407,'country':'us','state':'GA'},'full_clean'),
        # # ({'latitude':92.6407,'country':'us','state':'GA'},'save'),
        ({'latitude':-92.6407},'full_clean'),
        ({'longitude':-184.4277},'save'),
        ({'longitude':184.4277},'save'),
        ({'latitude':89.99},'full_clean'),
        ({'latitude':89.99},'save'),
        ({'timezone':'US/BlahBlah'},'full_clean'),
        ({'timezone':'US/BlahBlah'},'save'),
    ])
    def test_validators(self,kwargs,func,atl):

        #Change the info in the atl_dict and get the airport object
        atl.update(kwargs)
        airport = get_airport(**atl)

        #Only testing the validators...not the save
        with pytest.raises(ValidationError)  as excinfo:
            f = getattr(airport,func)
            f()

        # #Now test the create method
        # with pytest.raises(ValidationError)  as excinfo:
        #     create_airport(**atl)

    @pytest.mark.parametrize("tz",['US/Eastern','US/Mountain'])
    def test_timezone_codes(self,tz,tz_func,atl):
        atl.update({'timezone':tz_func(tz)})
        airport = create_airport(**atl)
        assert airport.get_tz_obj().zone == tz
        assert airport.get_tz_obj() == timezone.pytz.timezone(tz)
