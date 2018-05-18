import pytest
from rest_framework.test import APIClient
from query_flight.models import Airport, Flight, Layover
import pytz

@pytest.fixture
def apiclient():
    return APIClient()

# @pytest.fixture(params=['US/Eastern',pytz.timezone('US/Eastern')])
# def atl(request):
#     return Airport.objects.create(title='Atlanta',abrev='ATL',
#         sw_airport=True,latitude=33.6407,
#         longitude=-84.4277,timezone = request.param)



def pytest_generate_tests(metafunc):
    if 'airport' in metafunc.fixturenames:
        metafunc.parametrize("airport", ['ATL', 'BOI'], indirect=True)

@pytest.fixture
def airport(request,tz):
    if request.param == 'ATL':
        return Airport.objects.create(title='Atlanta',abrev='ATL',
            sw_airport=True,latitude=33.6407,
            longitude=-84.4277,timezone = 'US/Eastern')
    elif request.param == 'BOI':
        return Airport.objects.create(title='Boise',abrev='BOI',
            sw_airport=True,latitude=43.5658,
            longitude=-116.2223,timezone = 'US/Mountain')
    else:
        raise ValueError("invalid internal test config")



# @pytest.fixture
# def boi():
#     return Airport.objects.create(title='Boise',abrev='BOI',
#         sw_airport=True,latitude=43.5658,
#         longitude=-116.2223,timezone = 'US/Mountain')
