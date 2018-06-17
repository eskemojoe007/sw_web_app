import pytest
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
# from rest_framework.test import APIClient
from query_flight.models import Airport, Flight, Layover, Search
# from .conftest import check_get, check_post


@pytest.fixture
def search_list():
    return reverse('query_flight:searchs-list')


@pytest.mark.django_db
def test_search_list(apiclient, search_list):
    response = apiclient.get(search_list)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_search_list(apiclient, search_list):
    response = apiclient.get(search_list)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_get_search(apiclient, search_list):
    response = apiclient.post(search_list)
    assert response.status_code == status.HTTP_201_CREATED
    assert Search.objects.count() == 1

    # Make sure it saved and put it self into the test db
    search = Search.objects.get()
    assert search.id == 1
    assert search.time <= timezone.now()

    # Now pull the list from the site
    response = apiclient.get(search_list)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.data[0].get('id') == search.id

    # Now get it individually
    response = apiclient.get(
        reverse('query_flight:searchs-detail', args=[search.id]))
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('id') == search.id


@pytest.mark.django_db
@pytest.mark.parametrize('n', [3, 6, 9])
def test_num_flights(apiclient, search_list, basic_flight_dict, n):

    for i in range(n):
        Flight.objects.create(**basic_flight_dict)

    response = apiclient.get(reverse('query_flight:searchs-detail', args=[1]))

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('num_flights') == n
