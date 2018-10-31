import pytest
from rest_framework import status
from django.urls import reverse


@pytest.fixture
def register_url():
    return reverse('sw_app:user-register')


@pytest.fixture
def login_url():
    return reverse('sw_app:user-login')


@pytest.fixture
def user_url():
    return reverse('sw_app:user')


@pytest.mark.django_db
class TestUserAuth(object):

    def test_create_user(self, register_url, User, apiclient, email, password):
        response = apiclient.post(register_url, {'email': email, 'password': password})
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        assert response.data['user'].get('email') == email
        assert response.data['user'].get('password') is None
        assert response.data.get('token') is not None
        assert response.data['user'].get('id') == 1

    @pytest.mark.parametrize('bad_email', [
        'bad email address',
        'cool@.com',
        'sweet.com',
        '@coo.com'
    ])
    def test_bad_email(self, register_url, User, apiclient, bad_email, password):
        response = apiclient.post(register_url, {'email': bad_email, 'password': password})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert User.objects.count() == 0
        assert 'email' in str(response.json())

    def test_unique_email(self, register_url, User, apiclient, email, password):
        response = apiclient.post(register_url, {'email': email, 'password': password})
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        response = apiclient.post(register_url, {'email': email, 'password': password})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert User.objects.count() == 1
        assert 'email' in str(response.json())

    def test_login(self, typical_user, email, password, apiclient, login_url):
        response = apiclient.post(login_url, {'email': email, 'password': password})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user'].get('email') == email
        assert response.data['user'].get('password') is None
        assert response.data.get('token') is not None

    def test_bad_login(self, typical_user, email, apiclient, login_url):
        response = apiclient.post(login_url, {'email': email, 'password': 'badpass'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'credentials' in str(response.json())

    def test_user(self, typical_user, email, password, apiclient, login_url, user_url):
        response = apiclient.post(login_url, {'email': email, 'password': password})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user'].get('email') == email
        assert response.data['user'].get('password') is None
        assert response.data.get('token') is not None
        assert response.data['user'].get('id') == 1

        apiclient.post(user_url, )
