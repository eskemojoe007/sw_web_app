import pytest
from rest_framework.test import APIClient
from rest_framework import status
from query_flight.models import Airport, Flight, Layover
import pytz

@pytest.fixture(scope='session')
def apiclient():
    return APIClient()

# @pytest.fixture(params=['US/Eastern',pytz.timezone('US/Eastern')])
# def atl(request):
#     return Airport.objects.create(title='Atlanta',abrev='ATL',
#         sw_airport=True,latitude=33.6407,
#         longitude=-84.4277,timezone = request.param)

@pytest.fixture(params=[str,pytz.timezone])
def time_func(request):
    return request.param

def pytest_generate_tests(metafunc):
    if 'airport' in metafunc.fixturenames:
        metafunc.parametrize("airport", ['ATL', 'BOI'], indirect=True)

@pytest.fixture(scope='function')
def atl(request):
    return Airport(title='Atlanta',abrev='ATL',
        sw_airport=True,latitude=33.6407,
        longitude=-84.4277,timezone = 'US/Eastern')

@pytest.fixture(scope='function')
def boi(request):
    return Airport(title='Boise',abrev='BOI',
        sw_airport=True,latitude=43.5658,
        longitude=-116.2223,timezone = pytz.timezone('US/Mountain'))

@pytest.fixture
def airport(request,atl,boi):
    if request.param == 'ATL':
        atl.save()
        return atl
    elif request.param == 'BOI':
        boi.save()
        return boi
    else:
        raise ValueError("invalid internal test config")

@pytest.fixture
def flight(request,airport):
        # a = create_atl()
        # b = create_atl(title='Boise',abrev='BOI',sw_airport=True,latitude=43.5658,
        #     longitude=-116.2223,timezone = 'US/Mountain')
        # return Flight(origin_airport=a,destination_airport=b,
        #     depart_time=a.get_tz_obj().localize(timezone.datetime(2018,4,26,6,00,00)),
        #     arrive_time=b.get_tz_obj().localize(timezone.datetime(2018,4,26,13,50,00)),
        #     wanna_get_away=438.0,anytime=571.0,business_select=599.0)
    print(airport.abrev)


def check_get(response):
    assert status.is_success(response.status_code)
    assert response.status_code == status.HTTP_200_OK
def check_post(response):
    assert status.is_success(response.status_code)
    assert response.status_code == status.HTTP_201_CREATED


# @pytest.fixture
# def boi():
#     return Airport.objects.create(title='Boise',abrev='BOI',
#         sw_airport=True,latitude=43.5658,
#         longitude=-116.2223,timezone = 'US/Mountain')
