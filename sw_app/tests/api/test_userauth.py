import pytest
from rest_framework import status
from django.urls import reverse


@pytest.fixture
def user_post():
    return reverse('sw_app:user-post')


@pytest.mark.django_db
class TestUserAuth(object):

    def test_create_user(self, user_post, User, apiclient, email, password):
        response = apiclient.post(user_post, {'email': email, 'password': password})
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
    def test_bad_email(self, user_post, User, apiclient, bad_email, password):
        response = apiclient.post(user_post, {'email': bad_email, 'password': password})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert User.objects.count() == 0
        assert 'email' in str(response.json())
