import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestUser(object):

    def test_basic_login(self, typical_user, typical_login, email):
        assert typical_user.email == email
        assert typical_login is True

    def test_bad_login(self, client, typical_user):
        login = client.login(email=typical_user.email, password='badpass')
        assert login is False

    def test_change_password(self, typical_user, client):
        new_pass = 'newPassword'
        typical_user.set_password(new_pass)
        typical_user.save()

        assert client.login(email=typical_user.email, password=new_pass)

    @pytest.mark.xfail
    def test_bad_email(self, password):
        # TODO: Make this actually run!
        email = 'invalid email address'
        with pytest.raises(ValidationError):
            user = get_user_model().objects.create(email=email, password=password)
            print(user.email)
            # User = get_user_model()
            # user = User(email=email)
            # user.full_clean()
