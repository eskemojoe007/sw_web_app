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
def test_flight_list(apiclient, flight_list):
    response = apiclient.get(flight_list)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_get_flight(apiclient, flight_list, post_flight_dict):
    response = apiclient.post(flight_list, post_flight_dict)
    assert response.status_code == status.HTTP_201_CREATED
    assert Flight.objects.count() == 1

    # Make sure it saved and put it self into the test db
    flight = Flight.objects.get()
    assert flight.destination_airport.abrev == post_flight_dict['destination_airport']
    assert flight.travel_time(
    ) == post_flight_dict['arrive_time'] - post_flight_dict['depart_time']
    assert flight.min_price() == post_flight_dict['wanna_get_away']
    assert flight.wanna_get_away == post_flight_dict['wanna_get_away']

    # Now pull the list from the site
    response = apiclient.get(flight_list)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.data[0].get('wanna_get_away') == flight.wanna_get_away
    assert response.data[0].get('min_price') == flight.min_price()
    assert response.data[0].get('travel_time') == flight.travel_time()
    # assert response.data[0].get('num_layovers') == flight.num_layovers()

    # Now get it individually
    response = apiclient.get(
        reverse('query_flight:flights-detail', args=[flight.id]))
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('wanna_get_away') == flight.wanna_get_away
    assert response.data.get('min_price') == flight.min_price()
    assert response.data.get('travel_time') == flight.travel_time()
    # assert response.data.get('num_layovers') == flight.num_layovers()


@pytest.mark.django_db
@pytest.mark.parametrize('kwargs', [
    {'origin_airport': 'BBB'},
    {'search': 27}
])
def test_post_bad_keys(apiclient, flight_list, post_flight_dict, kwargs):
    post_flight_dict.update(kwargs)
    response = apiclient.post(flight_list, post_flight_dict)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert list(kwargs.keys())[0] in str(response.json())
    assert "object does not exist" in str(response.json())


@pytest.mark.django_db
@pytest.mark.parametrize('kwargs,error_bool', [
    ({'wanna_get_away': -50}, True),
    ({'anytime': -50}, True),
    ({'business_select': -50}, True),
])
def test_post_bad_field(apiclient, flight_list, post_flight_dict, kwargs, error_bool):
    post_flight_dict.update(kwargs)
    response = apiclient.post(flight_list, post_flight_dict)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert list(kwargs.keys())[0] in str(response.json())


@pytest.mark.django_db
@pytest.mark.parametrize('kwargs', [
    {'origin_airport': 'ATL', 'destination_airport': 'ATL'},
    {'origin_airport': 'BOI', 'destination_airport': 'BOI'},
])
def test_post_same_airport(apiclient, flight_list, post_flight_dict, kwargs):
    post_flight_dict.update(kwargs)
    response = apiclient.post(flight_list, post_flight_dict)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert kwargs['origin_airport'] in str(response.json())


@pytest.mark.django_db
def test_post_times(apiclient, flight_list, post_flight_dict):

    # Reverse flight times
    post_flight_dict.update({'arrive_time': post_flight_dict['depart_time'],
                             'depart_time': post_flight_dict['arrive_time']})
    response = apiclient.post(flight_list, post_flight_dict)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'before' in str(response.json())
