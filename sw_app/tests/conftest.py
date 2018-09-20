import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def email():
    return 'testuser@test.com'


@pytest.fixture
def password():
    return '12345'


@pytest.fixture(scope='function')
def typical_user(email, password):
    return get_user_model().objects.create_user(email=email, password=password)


@pytest.fixture(scope='function')
def typical_login(client, typical_user, password):
    return client.login(email=typical_user.email, password=password)
