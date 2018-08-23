import pytest
from django.utils import timezone
from query_flight.models import Flight
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class Test_Flight_Model(object):

    @pytest.mark.parametrize('kwargs,expected', [
        ({'wanna_get_away': 100}, 100),
        ({'anytime': 100}, 100),
        ({'business_select': 100}, 100),
        ({}, None),
        ({'wanna_get_away': 100.00, 'business_select': 150.00}, 100.00),
        ({'anytime': 100.00, 'business_select': 150.00}, 100.00),
    ])
    def test_min_price(self, kwargs, expected):
        assert Flight(**kwargs).min_price() == expected

    @pytest.mark.parametrize('depart,arrive,expected', [
        (timezone.datetime(2018, 4, 22, 17, 00, 00), timezone.datetime(
            2018, 4, 22, 22, 00, 00), timezone.timedelta(hours=5)),
    ])
    def test_travel_time(self, depart, arrive, expected):
        assert Flight(depart_time=depart,
                      arrive_time=arrive).travel_time() == expected

    def test_travel_time_localize(self, atl_airport, boi_airport):

        depart = atl_airport.get_tz_obj().localize(
            timezone.datetime(2018, 5, 11, 6, 0, 0))
        arrive = boi_airport.get_tz_obj().localize(
            timezone.datetime(2018, 5, 11, 13, 50, 0))

        f = Flight(depart_time=depart, arrive_time=arrive)

        assert f.travel_time() == timezone.timedelta(hours=9, minutes=50)

    def test_airport_connection(self, basic_flight, search_case, atl_airport):

        assert basic_flight.origin_airport() == search_case.origin_airport
        assert basic_flight.destination_airport() == search_case.destination_airport
        assert basic_flight.origin_airport().abrev == atl_airport.abrev

    def test_tz_aware(self, basic_flight):
        '''
        Test the tz_aware of everything...so here we will build a real Flight
        Then test the timezone of everything.
        '''
        assert timezone.is_aware(basic_flight.depart_time)
        assert timezone.is_aware(basic_flight.arrive_time)

    @pytest.mark.parametrize('kwargs,error_bool', [
        ({'wanna_get_away': -50}, True),
        ({'anytime': -50}, True),
        ({'business_select': -50}, True),

    ])
    def test_validators1(self, basic_flight_dict, kwargs, error_bool):
        basic_flight_dict.update(kwargs)

        f = Flight(**basic_flight_dict)
        with pytest.raises(ValidationError):
            f.full_clean()

    # def test_airport_match(self, basic_flight_dict, atl_airport):
    #     basic_flight_dict.update({'origin_airport': atl_airport,
    #                               'destination_airport': atl_airport})
    #
    #     with pytest.raises(ValidationError):
    #         f = Flight.objects.create(**basic_flight_dict)

    def test_times(self, basic_flight_dict):
        basic_flight_dict.update({'arrive_time': basic_flight_dict['depart_time'],
                                  'depart_time': basic_flight_dict['arrive_time']})
        with pytest.raises(ValidationError):
            Flight.objects.create(**basic_flight_dict)
