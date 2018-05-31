import pytest
from django.urls import reverse
from rest_framework import status
# from rest_framework.test import APIClient
from query_flight.models import Airport, Flight, Layover, Search
# from .conftest import check_get, check_post

@pytest.fixture
def search_list():
    return reverse('query_flight:searchs-list')

@pytest.mark.django_db
def test_search_list(apiclient,search_list):
    response = apiclient.get(search_list)
    assert response.status_code == status.HTTP_200_OK
