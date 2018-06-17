import pytest
from django.utils import timezone
from query_flight.models import Airport, Flight, Search, Layover


@pytest.fixture(scope='function', params=[str, timezone.pytz.timezone])
def tz_func(request):
    return request.param


@pytest.fixture
def atl_dict():
    return {'title': 'Atlanta', 'abrev': 'ATL', 'sw_airport': True,
            'latitude': 33.6407, 'longitude': -84.4277,
            'timezone': 'US/Eastern'}


@pytest.fixture
def boi_dict():
    return {'title': 'Boise', 'abrev': 'BOI', 'sw_airport': True,
            'latitude': 43.5658, 'longitude': -116.2223, 'timezone': 'US/Mountain'}


@pytest.fixture
def dal_dict():
    return {'title': 'Dallas Love Field', 'abrev': 'DAL', 'sw_airport': True,
            'latitude': 32.8481, 'longitude': -96.8512, 'timezone': 'US/Central'}


@pytest.fixture
def aua_dict():
    return {'title': 'Aruba', 'abrev': 'AUA', 'sw_airport': True,
            'latitude': 12.501400, 'longitude': -70.015198, 'timezone': 'America/Aruba'}


@pytest.fixture
def atl_dict_total(atl_dict):
    atl_dict.update({'country': 'us', 'state': 'Georgia'})
    return atl_dict


@pytest.fixture
def boi_dict_total(boi_dict):
    boi_dict.update({'country': 'us', 'state': 'Idaho'})
    return boi_dict


@pytest.fixture
def dal_dict_total(dal_dict):
    dal_dict.update({'country': 'us', 'state': 'Texas'})
    return dal_dict


@pytest.fixture
def aua_dict_total(aua_dict):
    aua_dict.update({'country': 'nl'})
    return aua_dict


@pytest.fixture
def atl_airport(atl_dict_total):
    return Airport.objects.create(**atl_dict_total)


@pytest.fixture
def boi_airport(boi_dict_total):
    return Airport.objects.create(**boi_dict_total)


@pytest.fixture
def dal_airport(dal_dict_total):
    return Airport.objects.create(**dal_dict_total)


@pytest.fixture
def aua_airport(aua_dict_total):
    return Airport.objects.create(**aua_dict_total)


@pytest.fixture
def search():
    return Search.objects.create()


@pytest.fixture
def basic_flight_dict(atl_airport, boi_airport, search):
    return {'origin_airport': atl_airport, 'destination_airport': boi_airport,
            'depart_time': atl_airport.get_tz_obj().localize(timezone.datetime(2018, 4, 26, 6, 00, 00)),
            'arrive_time': boi_airport.get_tz_obj().localize(timezone.datetime(2018, 4, 26, 13, 50, 00)),
            'wanna_get_away': 438.0, 'anytime': 571.0, 'business_select': 599.0, 'search': search}


@pytest.fixture
def post_flight_dict(atl_airport, boi_airport, search):
    return {'origin_airport': atl_airport.abrev, 'destination_airport': boi_airport.abrev,
            'depart_time': atl_airport.get_tz_obj().localize(timezone.datetime(2018, 4, 26, 6, 00, 00)),
            'arrive_time': boi_airport.get_tz_obj().localize(timezone.datetime(2018, 4, 26, 13, 50, 00)),
            'wanna_get_away': 438.0, 'anytime': 571.0, 'business_select': 599.0, 'search': search.id}


@pytest.fixture
def basic_flight(basic_flight_dict):
    return Flight.objects.create(**basic_flight_dict)


@pytest.fixture
def post_layover_dict(basic_flight, dal_airport):
    return {'airport': dal_airport.abrev,
            'change_planes': True,
            'time': 3600.0}

# This gets all the airports for tests
# def pytest_generate_tests(metafunc):
#     if 'airports' in metafunc.fixturenames:
#         metafunc.parametrize("airports", ['atl','boi'], indirect=True)


@pytest.fixture(scope='function')
def airports(request, atl_airport, boi_airport, dal_airport, aua_airport):
    if request.param.lower() == 'atl':
        return atl_airport
    elif request.param.lower() == 'boi':
        return boi_airport
    elif request.param.lower() == 'dal':
        return dal_airport
    elif request.param.lower() == 'aua':
        return aua_airport
    else:
        raise ValueError('Invalid param in airports')


@pytest.fixture(scope='function')
def airports_dict(request, atl_dict_total, boi_dict_total, dal_dict_total, aua_dict_total):
    if request.param.lower() == 'atl':
        return atl_dict_total
    elif request.param.lower() == 'boi':
        return boi_dict_total
    elif request.param.lower() == 'dal':
        return dal_dict_total
    elif request.param.lower() == 'aua':
        return aua_dict_total
    else:
        raise ValueError('Invalid param in airports_dict')


@pytest.fixture(scope='function')
def airports_dict_partial(request, atl_dict, boi_dict, dal_dict, aua_dict):
    if request.param.lower() == 'atl':
        return atl_dict
    elif request.param.lower() == 'boi':
        return boi_dict
    elif request.param.lower() == 'dal':
        return dal_dict
    elif request.param.lower() == 'aua':
        return aua_dict
    else:
        raise ValueError('Invalid param in airports_dict')

# @pytest.fixture(scope='function')
# def airports(request,atl_dict_total,boi_dict_total,dal_dict_total):
#     if request.param.lower() == 'atl':
#         return Airport.objects.get_or_create(**atl_dict_total)
#     elif request.param.lower() == 'boi':
#         return Airport.objects.get_or_create(**boi_dict_total)
#     elif request.param.lower() == 'dal':
#         return Airport.objects.get_or_create(**dal_dict_total)
#     else:
#         raise ValueError('Invalid param in airports')
