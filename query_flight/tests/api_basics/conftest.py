import pytest
from rest_framework.test import APIClient
# from query_flight.models import Airport


@pytest.fixture(scope='session')
def apiclient():
    return APIClient()


@pytest.fixture
def basic_flight_post(basic_flight_dict):
    # TODO: Need to finish this...idea is to replace the real airport with just
    # the necessary information
    basic_flight_dict.update()
