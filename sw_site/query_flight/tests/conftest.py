import pytest
from django.utils import timezone

@pytest.fixture(scope='function',params=[str,timezone.pytz.timezone])
def tz_func(request):
    return request.param

@pytest.fixture
def atl():
    return {'title':'Atlanta','abrev':'ATL','sw_airport':True,
        'latitude':33.6407, 'longitude':-84.4277,
        'timezone': 'US/Eastern'}

@pytest.fixture
def atl_total():
    return {'title':'Atlanta','abrev':'ATL','sw_airport':True,
        'latitude':33.6407, 'longitude':-84.4277,
        'timezone': 'US/Eastern','country':'us','state':'Georgia'}

@pytest.fixture
def boi():
    return {'title':'Boise','abrev':'BOI','sw_airport':True,
        'latitude':43.5658,'longitude':-116.2223,'timezone':'US/Mountain'}
