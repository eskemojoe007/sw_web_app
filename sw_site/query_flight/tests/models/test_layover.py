import pytest
from django.utils import timezone
from query_flight.models import Flight, Airport, Layover
from django.core.exceptions import ValidationError

@pytest.mark.django_db
class Test_Layover_Model(object):

    @pytest.mark.parametrize('time_s',[60*60,90*60,20*60])
    def test_timedelta(self,time_s):
        l = Layover(time=time_s)
        assert l.timedelta().total_seconds() == time_s

    @pytest.mark.parametrize('airports,error_bool',[
        ('ATL',True),
        ('DAL',False),
        ('BOI',True),
        ('AUA',False),
        ],indirect=['airports'])
    def test_layover_location(self,airports,error_bool,basic_flight):
        l = Layover(airport=airports,flight=basic_flight,change_planes=True,time=60*60)
        if error_bool:
            with pytest.raises(ValidationError):
                l.full_clean()
        else:
            l.full_clean()
            l.save()
            assert basic_flight.num_layovers() == 1
