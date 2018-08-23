import pytest
# from django.utils import timezone
from query_flight.models import Layover
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class Test_Layover_Model(object):

    @pytest.mark.parametrize('time_s', [60 * 60, 90 * 60, 20 * 60])
    def test_timedelta(self, time_s):
        l_obj = Layover(time=time_s)
        assert l_obj.timedelta().total_seconds() == time_s

    @pytest.mark.parametrize('airports,error_bool', [
        ('ATL', True),
        ('DAL', False),
        ('BOI', True),
        ('AUA', False),
    ], indirect=['airports'])
    def test_layover_location(self, airports, error_bool, basic_flight):
        if error_bool:
            with pytest.raises(ValidationError):
                Layover.objects.create(
                    airport=airports, flight=basic_flight, change_planes=True, time=60 * 60)
        else:
            Layover.objects.create(
                airport=airports, flight=basic_flight, change_planes=True, time=60 * 60)
            assert basic_flight.num_layovers() == 1
