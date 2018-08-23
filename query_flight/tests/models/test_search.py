import pytest
from django.utils import timezone
from query_flight.models import Search, SearchCard, Flight, SearchCase
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

    @pytest.mark.parametrize('n1,n2,n3', [
        (1, 1, 1),
        (1, 5, 5),
        (5, 1, 2),
        (5, 5, 5),
        (random.randint(1, 10), random.randint(1, 10), random.randint(1, 10))
    ])
    def test_nums(self, search_case_dict, basic_flight_dict,
                  search, n1, n2, n3):

        assert search.num_cases() == 1
        assert search.num_cards() == 1
        assert search.num_flights() == 0

        for i in range(n1):
            s_card = SearchCard.objects.create(search=search)
            for j in range(n2):
                search_case_dict.update({'search_card': s_card})
                sc = SearchCase.objects.create(**search_case_dict)
                for j in range(n3):
                    basic_flight_dict.update({'search_case': sc})
                    Flight.objects.create(**basic_flight_dict)
                assert sc.num_flights() == n3
            assert s_card.num_flights() == n2 * n3
            assert s_card.num_cases() == n2
        assert search.num_flights() == n1 * n2 * n3

        # Add 1 for the initially created ones
        assert search.num_cards() == n1 + 1
        assert search.num_cases() == n1 * n2 + 1
