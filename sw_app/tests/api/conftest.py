import pytest
from rest_framework.test import APIClient


@pytest.fixture(scope='function')
def apiclient():
    return APIClient()
