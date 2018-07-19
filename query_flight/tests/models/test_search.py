import pytest
from django.utils import timezone
from query_flight.models import Search, Flight
import random


@pytest.mark.django_db
class Test_Search_Model(object):

    def test_time_now(self):
        n = timezone.now()
        s = Search.objects.create()
        assert s.time >= n

    def test_time_input(self):
        '''We should not be able to set it differently...just leave it alone'''
        n = timezone.now()
        s = Search.objects.create(time=n + timezone.timedelta(hours=5))
        assert s.time >= n

    def test_number_flights(self, basic_flight_dict, search):
        n = random.randint(1, 10)
        for i in range(n):
            Flight.objects.create(**basic_flight_dict)
        assert search.num_flights() == n
