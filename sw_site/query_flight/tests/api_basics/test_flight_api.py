import pytest
from django.urls import reverse
from rest_framework import status
# from rest_framework.test import APIClient
from query_flight.models import Airport, Flight, Layover
# from .conftest import check_get, check_post

@pytest.fixture
def flight_list():
    return reverse('query_flight:flights-list')

@pytest.mark.django_db
def test_flight_list(apiclient,flight_list):
    response = apiclient.get(flight_list)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_post_get_flight(apiclient,flight_list,basic_flight_dict):
    response = apiclient.post(flight_list,basic_flight_dict)
    assert response.status_code == status.HTTP_201_CREATED
    assert Flight.objects.count() == 1

    # Make sure it saved and put it self into the test db
    flight = Flight.objects.get()
    assert flight.destination_airport.abrev == basic_flight_dict['destination_airport'].abrev
    assert flight.travel_time == basic_flight_dict['travel_time']
    assert flight.min_price == basic_flight_dict['min_price']
    assert flight.wanna_get_away == basic_flight_dict['wanna_get_away']

    # Now pull the list from the site
    response = apiclient.get(flight_list)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.data[0].get('wanna_get_away') == flight.wanna_get_away
    assert response.data[0].get('min_price') == flight.min_price
    assert response.data[0].get('travel_time') == flight.travel_time

    # Now get it individually
    response = apiclient.get(reverse('query_flight:flights-detail',args=[flight.id]))
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('wanna_get_away') == flight.wanna_get_away
    assert response.data.get('min_price') == flight.min_price
    assert response.data.get('travel_time') == flight.travel_time
