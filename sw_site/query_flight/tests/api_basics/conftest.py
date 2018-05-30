import pytest
from rest_framework.test import APIClient
from query_flight.models import Airport

@pytest.fixture(scope='session')
def apiclient():
    return APIClient()
