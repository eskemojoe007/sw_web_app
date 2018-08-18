import pytest
# from django.utils import timezone
from query_flight.models import SearchCard, Flight
import random


@pytest.mark.django_db
class Test_SearchCard_Model(object):

    @pytest.mark.parametrize('n', [
        1, 5, 10, random.randint(1, 10)
    ])
    def test_number_flights(self, basic_flight_dict, search_card, n):
        for i in range(n):
            Flight.objects.create(**basic_flight_dict)
        assert search_card.num_flights() == n
