import pytest
from django.urls import reverse
from rest_framework import status
from query_flight.models import Airport
import pytz
from .conftest import check_get, check_post


@pytest.fixture
def airport_list():
    return reverse('query_flight:airports-list')

@pytest.mark.django_db
def test_airport_list(apiclient,airport_list):
    response = apiclient.get(airport_list)
    check_get(response)

@pytest.mark.django_db
def test_create_airport(apiclient,airport_list,atl):
    params = {
        'title':'Atlanta',
        'timezone':'US/Eastern',
        'abrev':'ATL',
        'latitude':33.6407,
        'longitude':-84.4277,
        'sw_airport':True,
    }
    response = apiclient.post(airport_list,params)
    check_post(response)
    assert Airport.objects.count() == 1
    airport = Airport.objects.get()
    assert airport.title == 'Atlanta'
    assert airport.get_tz_obj().zone == 'US/Eastern'
    assert airport.get_tz_obj() == pytz.timezone('US/Eastern')

@pytest.mark.django_db
def test_get_airports(apiclient,airport_list,airport):
    assert Airport.objects.count() == 1

    response = apiclient.get(airport_list)
    check_get(response)
    assert len(response.json()) == 1
    assert response.data[0].get('title') == airport.title
    assert response.data[0].get('abrev') == airport.abrev
    assert response.data[0].get('timezone') == airport.get_tz_obj().zone

@pytest.mark.django_db
def test_get_airport(apiclient,airport):
    assert Airport.objects.count() == 1

    response = apiclient.get(reverse('query_flight:airports-detail',args=[airport.abrev]))
    check_get(response)
    assert response.data.get('title') == airport.title
    assert response.data.get('abrev') == airport.abrev
    assert response.data.get('timezone') == airport.get_tz_obj().zone
