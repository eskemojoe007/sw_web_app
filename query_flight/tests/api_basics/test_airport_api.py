import pytest
from django.urls import reverse
from rest_framework import status
from query_flight.models import Airport
from query_flight.serializers import AirportSerializer
import pytz
# from .conftest import check_get, check_post


@pytest.fixture
def airport_list():
    return reverse('query_flight:airports-list')


@pytest.mark.django_db
def test_airport_list(apiclient, airport_list):
    response = apiclient.get(airport_list)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.parametrize('airports_dict', ['ATL', 'BOI', 'DAL'], indirect=True)
def test_get_airports(apiclient, airport_list, airports_dict):
    response = apiclient.post(airport_list, airports_dict)
    assert response.status_code == status.HTTP_201_CREATED
    assert Airport.objects.count() == 1

    # Make sure it saved and put it self into the test db
    airport = Airport.objects.get()
    assert airport.title == airports_dict['title']
    assert airport.get_tz_obj().zone == airports_dict['timezone']
    assert airport.get_tz_obj() == pytz.timezone(airports_dict['timezone'])

    # Now pull the list from the site
    response = apiclient.get(airport_list)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.data[0].get('title') == airport.title
    assert response.data[0].get('abrev') == airport.abrev
    assert response.data[0].get('timezone') == airport.get_tz_obj().zone

    # Now get it individually
    response = apiclient.get(
        reverse('query_flight:airports-detail', args=[airport.abrev]))
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('title') == airport.title
    assert response.data.get('abrev') == airport.abrev
    assert response.data.get('timezone') == airport.get_tz_obj().zone


@pytest.mark.django_db
@pytest.mark.parametrize("kwargs", [
    ({'latitude': 92.6407}),
    ({'latitude': -92.6407}),
    ({'longitude': -184.4277}),
    ({'longitude': 184.4277}),
    ({'timezone': 'US/BlahBlah'}),
])
def test_field_validators(apiclient, kwargs, airport_list, atl_dict):
    # Change the info in the atl_dict_dict and get the airport object
    atl_dict.update(kwargs)
    response = apiclient.post(airport_list, atl_dict)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert list(kwargs)[0] in str(response.json())


@pytest.mark.django_db
@pytest.mark.parametrize('airports_dict_partial,country,state',
                         [
                             ('ATL', 'us', 'Georgia'),
                             ('BOI', 'us', 'Idaho'),
                             ('DAL', 'us', 'Texas'),
                             ('AUA', 'nl', None),
                         ], indirect=['airports_dict_partial'])
def test_serializer_validate(airports_dict_partial, country, state):
    serializer = AirportSerializer(data=airports_dict_partial)

    assert serializer.is_valid()
    assert serializer.validated_data['country'] == country
    assert serializer.validated_data.get('state') == state


@pytest.mark.django_db
@pytest.mark.parametrize('airports_dict_partial,country',
                         [
                             ('ATL', 'us'),
                             ('BOI', 'us'),
                             ('DAL', 'us'),
                             ('AUA', 'nl'),
                         ], indirect=['airports_dict_partial'])
def test_loc_validator(apiclient,
                       airport_list,
                       airports_dict_partial,
                       country):
    response = apiclient.post(airport_list, airports_dict_partial)
    assert response.status_code == status.HTTP_201_CREATED
    assert Airport.objects.count() == 1

    # Make sure it saved and put it self into the test db
    airport = Airport.objects.get()
    assert airport.country == country

    # print(airports_dict_partial)
    # assert response.status_code == status.HTTP_400_BAD_REQUEST
    # assert "country" in str(response.json())


@pytest.mark.django_db
@pytest.mark.parametrize("kwargs", [
    # ({'latitude':92.6407}),
    # ({'latitude':-92.6407}),
    # ({'longitude':-184.4277}),
    # ({'longitude':184.4277}),
    ({'latitude': 89.99}),
    ({'latitude': -89.99}),
])
def test_geo_validators(apiclient, kwargs, airport_list, atl_dict):
    # Change the info in the atl_dict_dict and get the airport object
    atl_dict.update(kwargs)
    response = apiclient.post(airport_list, atl_dict)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Geolocator' in str(response.json())
