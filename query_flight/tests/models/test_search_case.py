import pytest
# from django.utils import timezone
from query_flight.models import SearchCard, Flight, Search, SearchCase
import random
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class Test_SearchCase_Model(object):

    def test_create_search(self, search_case_dict):

        # fixtures should be created
        assert SearchCard.objects.count() == 1
        assert Search.objects.count() == 1

        # Create from the fixture...and attach to the existing fixture
        SearchCase.objects.create(**search_case_dict)

        assert SearchCase.objects.count() == 1
        assert SearchCard.objects.count() == 1
        assert Search.objects.count() == 1

        # Try again
        SearchCase.objects.create(**search_case_dict)
        assert SearchCase.objects.count() == 2
        assert SearchCard.objects.count() == 1
        assert Search.objects.count() == 1

        assert Search.objects.all()[0].num_cards() == 1
        assert SearchCard.objects.all()[0].num_cases() == 2

        # Remove the search Card to see if it can make one by default
        search_case_dict.pop('search_card', None)
        SearchCase.objects.create(**search_case_dict)
        assert SearchCase.objects.count() == 3
        assert SearchCard.objects.count() == 2
        assert Search.objects.count() == 2

        # Add back in the search, but not search CARD
        search_case_dict['search'] = Search.objects.all()[0]
        print(search_case_dict)
        SearchCase.objects.create(**search_case_dict)
        assert SearchCase.objects.count() == 4
        assert SearchCard.objects.count() == 3
        assert Search.objects.count() == 2
        assert Search.objects.all()[0].num_cards() == 2

    def test_airport_match(self, search_case_dict, atl_airport):
        search_case_dict.update({'origin_airport': atl_airport,
                                 'destination_airport': atl_airport})

        with pytest.raises(ValidationError):
            SearchCase.objects.create(**search_case_dict)

    @pytest.mark.parametrize('n', [
        1, 5, 10, random.randint(1, 10)
    ])
    def test_number_flights(self, basic_flight_dict, search_card, n):
        for i in range(n):
            Flight.objects.create(**basic_flight_dict)
        assert search_card.num_flights() == n
