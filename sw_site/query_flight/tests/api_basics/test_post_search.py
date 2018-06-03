import pytest
from django.urls import reverse
from rest_framework import status
from query_flight.serializers import SearchPostSerializer
from django.utils import timezone
from query_flight.models import Airport, Flight, Layover, Search

@pytest.fixture
def search_url():
    return reverse('query_flight:search-post')

@pytest.fixture
def basic_search(boi_airport,atl_airport):
    return {'destinationAirportCode':'BOI',
        'originationAirportCode':'ATL',
        'departureDate':timezone.now().date() + timezone.timedelta(days=5),
        'returnDate':timezone.now().date() + timezone.timedelta(days=10),
        }

def test_get(apiclient,search_url):
    response = apiclient.get(search_url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

@pytest.mark.django_db
@pytest.mark.parametrize('kwargs,error',[
    ({'destinationAirportCode':'boi'},False),
    ({'destinationAirportCode':'BOI'},False),
    ({'destinationAirportCode':'AtL'},False),
    ({'destinationAirportCode':'aTL'},False),
    ({'destinationAirportCode':'bbb'},True),
    ({'originationAirportCode':'boi'},False),
    ({'originationAirportCode':'BOI'},False),
    ({'originationAirportCode':'AtL'},False),
    ({'originationAirportCode':'aTL'},False),
    ({'originationAirportCode':'bbb'},True),
    ({'departureDate':timezone.now().date() - timezone.timedelta(days=5)},True),
    ({'departureDate':timezone.now().date() + timezone.timedelta(days=5)},False),
    # ({'returnDate':timezone.now().date() + timezone.timedelta(days=100)},False),
    # ({'returnDate':timezone.now().date() - timezone.timedelta(days=100)},True),
    # ({'departureDate':timezone.now().date() + timezone.timedelta(days=5),
    #   'returnDate':timezone.now().date() + timezone.timedelta(days=3)},True),
    # ({'departureDate':timezone.now().date() + timezone.timedelta(days=5),
    #   'returnDate':timezone.now().date() + timezone.timedelta(days=7)},False),
])
def test_validators_no_post(basic_search,kwargs,error):
    basic_search.update(kwargs)

    s = SearchPostSerializer(data=basic_search)
    assert s.is_valid() != error


# TODO: This test requires that we have all the airports loaded...wont work.
# hard to keep repeatable with the southwest website too.
# @pytest.mark.django_db
# def test_full_api(apiclient,search_url,basic_search):
#
#         response = apiclient.post(search_url,basic_search)
#         assert response.status_code == status.HTTP_201_CREATED
#         assert Search.objects.count() == 1
#         assert Flight.objects.count() >= 1
