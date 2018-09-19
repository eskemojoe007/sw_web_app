import pytest


@pytest.mark.django_db
class TestAirportModel(object):
    def test_autofail(self):
        assert False
