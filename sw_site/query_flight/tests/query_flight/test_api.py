import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from query_flight.models import Airport, Flight, Layover

class TestAirport(APITestCase):
    def set_up(self):
        self.client = APIClient()
        self.url = reverse('query_flight:airport-list')

    def test_airport_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200,
            'Expected Response Code 200, received {} instead.'
            .format(response.status_code))

    @pytest.mark.django_db
    def test_airport_list_real(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200,
            'Expected Response Code 200, received {} instead.'
            .format(response.status_code))
        # TODO: Find GSP in the list

    def test_create_airport(self):
        params = {
            'title':'Atlanta',
            'timezone':'US/Eastern',
            'abrev':'ATL',
            'latitude':33.6407,
            'longitude':-84.4277,
            'sw_airport':True,
        }
        response = self.client.post(self.url,params)
        self.assertEqual(response.status_code, 201,
            'Expected Response Code 201, received {0} instead.'
            .format(response.status_code))

        response = self.client.get(self.url)
        # TODO: Check if ATL is in that list

    def test_get_single_airport(self):
        pass
    def test_update_airport(self):
        pass
    def test_partial_update_airport(self):
        pass
    def test_destroy_airport(self):
        pass
