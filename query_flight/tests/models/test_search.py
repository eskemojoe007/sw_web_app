import pytest
from django.utils import timezone
from query_flight.models import Search, SearchCard, Flight
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

    @pytest.mark.parametrize('n', [
        1, 5, 10, random.randint(1, 10)
    ])
    def test_num_search_card(self, search, n):
        for i in range(n):
            SearchCard.objects.create(search=search)
        assert search.num_cards() == n

    # @pytest.mark.parametrize('n1,n2', [
    #     (1, 1),
    #     (1, 5),
    #     (5, 1),
    #     (5, 5),
    #     (random.randint(1, 10), random.randint(1, 10))
    # ])
    # def test_num_flights(self, search, basic_flight_dict, n1, n2):
    #     for i in range(n1):
    #         sc = SearchCard.objects.create(search=search)
    #         for i in range(n2):
    #             basic_flight_dict.update({'search_card': sc})
    #             Flight.objects.create(**basic_flight_dict)
    #
    #         assert sc.num_flights() == n2
    #     assert search.num_flights() == n1*n2

    # def test_number_flights(self, basic_flight_dict, search):
    #     n = random.randint(1, 10)
    #     for i in range(n):
    #         Flight.objects.create(**basic_flight_dict)
    #     assert search.num_flights() == n
