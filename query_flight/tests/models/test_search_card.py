import pytest
# from django.utils import timezone
from query_flight.models import Flight, SearchCase
import random


@pytest.mark.django_db
class Test_SearchCard_Model(object):

    @pytest.mark.parametrize('n1,n2', [
        (1, 1),
        (1, 5),
        (5, 1),
        (5, 5),
        (random.randint(1, 10), random.randint(1, 10))
    ])
    def test_num_flights(self, search_case_dict, basic_flight_dict, search_card, n1, n2):
        assert search_card.num_cases() == 1

        for i in range(n1):
            sc = SearchCase.objects.create(**search_case_dict)
            for j in range(n2):
                basic_flight_dict.update({'search_case': sc})
                Flight.objects.create(**basic_flight_dict)
            assert sc.num_flights() == n2
        assert search_card.num_flights() == n1*n2

        # using basic_flight_dict creates an empty SearchCase to attach to...
        # so we have 1 extra with no attached flights.
        assert search_card.num_cases() == n1 + 1

    @pytest.mark.parametrize('n', [
        1, 5, 10, random.randint(1, 10)
    ])
    def test_num_cases(self, search_case_dict, search_card, n):
        for i in range(n):
            SearchCase.objects.create(**search_case_dict)
        assert search_card.num_cases() == n

    def test_airports(self, search_card, search_case, search_case_dict):
        assert search_card.num_cases() == 1
        assert search_card.origins() == ['ATL']
        assert search_card.destinations() == ['BOI']

        # Add a duplicate case
        SearchCase.objects.create(**search_case_dict)
        assert search_card.num_cases() == 2
        assert search_card.origins() == ['ATL']
        assert search_card.destinations() == ['BOI']

        # Now switch and add
        search_case_dict.update({'origin_airport': search_case_dict['destination_airport'],
                                 'destination_airport': search_case_dict['origin_airport']})
        SearchCase.objects.create(**search_case_dict)
        assert search_card.num_cases() == 3
        assert set(search_card.origins()) == set(['ATL', 'BOI'])
        assert set(search_card.destinations()) == set(['ATL', 'BOI'])
