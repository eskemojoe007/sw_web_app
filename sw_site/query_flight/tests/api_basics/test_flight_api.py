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
def test_flight(apiclient,flight_list):
    response = apiclient.get(flight_list)
    assert response.status_code == status.HTTP_200_OK
    assert False
