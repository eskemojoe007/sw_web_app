import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from query_flight.models import Airport, Flight, Layover
import pytz

class check_status(APITestCase):
    def check_get(self,response):
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            'Expected Response Code 200, received {} instead.'
            .format(response.status_code))
    def check_create(self,response):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            'Expected Response Code 201, received {} instead.'
            .format(response.status_code))

class TestAirport(check_status):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('query_flight:airports-list')

    def test_airport_list(self):
        response = self.client.get(self.url)
        self.check_get(response)

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
        self.check_create(response)
        self.assertEqual(Airport.objects.count(),1)
        self.assertEqual(Airport.objects.get().title,'Atlanta')
        self.assertEqual(Airport.objects.get().timezone.zone,'US/Eastern')
        self.assertEqual(Airport.objects.get().timezone,pytz.timezone('US/Eastern'))

        # Can't be its own test for some unkown reason
        # def test_get_airport(self):
        response = self.client.get(reverse('query_flight:airports-detail',args=['ATL']))
        self.check_get(response)
        self.assertEqual(response.data.get('title'),'Atlanta')
        self.assertEqual(response.data.get('timezone'),'US/Eastern')

class TestFlight(check_status):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('query_flight:flights-list')

    def test_flight_list(self):
        response = self.client.get(self.url)
        self.check_get(response)

    def test_create_flight(self):
        pass
        # params = {
        #     'title':'Atlanta',
        #     'timezone':'US/Eastern',
        #     'abrev':'ATL',
        #     'latitude':33.6407,
        #     'longitude':-84.4277,
        #     'sw_airport':True,
        # }
        # response = self.client.post(self.url,params)
        # self.check_create(response)
        # self.assertEqual(Flight.objects.count(),1)
        # self.assertEqual(Flight.objects.get().title,'Atlanta')
        # self.assertEqual(Flight.objects.get().timezone.zone,'US/Eastern')
        # self.assertEqual(Flight.objects.get().timezone,pytz.timezone('US/Eastern'))

        # Can't be its own test for some unkown reason
        # def test_get_airport(self):
        # response = self.client.get(reverse('query_flight:airports-detail',args=['ATL']))
        # self.check_get(response)
        # self.assertEqual(response.data.get('title'),'Atlanta')
        # self.assertEqual(response.data.get('timezone'),'US/Eastern')
