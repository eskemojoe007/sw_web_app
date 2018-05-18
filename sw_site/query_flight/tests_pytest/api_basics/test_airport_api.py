import pytest
from django.urls import reverse
from rest_framework import status
# from rest_framework.test import APIClient
from query_flight.models import Airport, Flight, Layover
import pytz


# @pytest.fixture
# def apiclient():
#     return APIClient()

@pytest.fixture
def airport_list():
    return reverse('query_flight:airports-list')

# @pytest.fixture
# def atl():
#     return Airport.objects.create(title='Atlanta',abrev='ATL',
#         sw_airport=True,latitude=33.6407,
#         longitude=-84.4277,timezone = 'US/Eastern')

def check_get_code(status_code):
    return status_code == 200
def check_post_code(status_code):
    return status_code == 201

@pytest.mark.django_db
def test_airport_list(apiclient,airport_list):
    response = apiclient.get(airport_list)
    assert check_get_code(response.status_code)
    assert False

@pytest.mark.django_db
def test_create_airport(apiclient,airport_list):
    params = {
        'title':'Atlanta',
        'timezone':'US/Eastern',
        'abrev':'ATL',
        'latitude':33.6407,
        'longitude':-84.4277,
        'sw_airport':True,
    }
    response = apiclient.post(airport_list,params)
    assert check_post_code(response.status_code)
    assert Airport.objects.count() == 1
    airport = Airport.objects.get()
    assert airport.title == 'Atlanta'
    assert airport.get_tz_obj().zone == 'US/Eastern'
    assert airport.get_tz_obj() == pytz.timezone('US/Eastern')
    assert False

@pytest.mark.django_db
# @pytest.mark.parametrize("airport",[atl,boi])
def test_get_airports(apiclient,airport_list,airport):
    assert Airport.objects.count() == 1

    response = apiclient.get(airport_list)
    assert check_get_code(response.status_code)
    assert len(response.json()) == 1
    assert response.data[0].get('title') == airport.title
    assert response.data[0].get('abrev') == airport.abrev
    assert response.data[0].get('timezone') == airport.get_tz_obj().zone
    assert False


@pytest.mark.django_db
def test_get_airport(apiclient,airport):
    assert Airport.objects.count() == 1

    response = apiclient.get(reverse('query_flight:airports-detail',args=[airport.abrev]))
    assert check_get_code(response.status_code)
    assert response.data.get('title') == airport.title
    assert response.data.get('abrev') == airport.abrev
    assert response.data.get('timezone') == airport.get_tz_obj().zone
    assert False
