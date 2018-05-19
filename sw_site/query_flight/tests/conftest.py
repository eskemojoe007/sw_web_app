import pytest
from django.utils import timezone
from query_flight.models import Airport, Flight, Search, Layover

@pytest.fixture(scope='function',params=[str,timezone.pytz.timezone])
def tz_func(request):
    return request.param

@pytest.fixture
def atl_dict():
    return {'title':'Atlanta','abrev':'ATL','sw_airport':True,
        'latitude':33.6407, 'longitude':-84.4277,
        'timezone': 'US/Eastern'}

@pytest.fixture
def boi_dict():
    return {'title':'Boise','abrev':'BOI','sw_airport':True,
        'latitude':43.5658,'longitude':-116.2223,'timezone':'US/Mountain'}

@pytest.fixture
def dal_dict():
    return {'title':'Dallas Love Field','abrev':'DAL','sw_airport':True,
        'latitude':32.8481,'longitude':-96.8512,'timezone':'US/Central'}

@pytest.fixture
def atl_airport(atl_dict):
    return Airport.objects.create(**atl_dict)

@pytest.fixture
def boi_airport(boi_dict):
    return Airport.objects.create(**boi_dict)

@pytest.fixture
def dal_airport(dal_dict):
    return Airport.objects.create(**dal_dict)

@pytest.fixture
def search():
    return Search.objects.create()

@pytest.fixture
def basic_flight_dict(atl_airport,boi_airport,search):
    return {'origin_airport':atl_airport,'destination_airport':boi_airport,
        'depart_time':atl_airport.get_tz_obj().localize(timezone.datetime(2018,4,26,6,00,00)),
        'arrive_time':boi_airport.get_tz_obj().localize(timezone.datetime(2018,4,26,13,50,00)),
        'wanna_get_away':438.0,'anytime':571.0,'business_select':599.0,'search':search}

@pytest.fixture
def basic_flight(basic_flight_dict):
    return Flight.objects.create(**basic_flight_dict)

# This gets all the airports for tests
# def pytest_generate_tests(metafunc):
#     if 'airports' in metafunc.fixturenames:
#         metafunc.parametrize("airports", ['atl','boi'], indirect=True)

@pytest.fixture
def airports(request,atl_airport,boi_airport,dal_airport):
    if request.param.lower() == 'atl':
        return atl_airport
    elif request.param.lower() == 'boi':
        return boi_airport
    elif request.param.lower() == 'dal':
        return dal_airport
    else:
        raise ValueError('Invalid param in airports')
