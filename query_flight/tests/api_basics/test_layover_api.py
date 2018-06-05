import pytest
from django.urls import reverse
from rest_framework import status
# from rest_framework.test import APIClient
from query_flight.models import Airport, Flight, Layover
# from .conftest import check_get, check_post

@pytest.fixture
def layover_list(basic_flight):
    return reverse('query_flight:layovers-list',args=[basic_flight.id])



@pytest.mark.django_db
def test_layovers_list(apiclient,layover_list):
    response = apiclient.get(layover_list)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_post_get_layover(apiclient,layover_list,post_layover_dict):
    response = apiclient.post(layover_list,post_layover_dict)
    assert response.status_code == status.HTTP_201_CREATED
    assert Layover.objects.count() == 1
    assert Flight.objects.count() == 1
    assert Airport.objects.count() == 3

    # Make sure it saved and put it self into the test db
    layover = Layover.objects.get()
    assert layover.airport.abrev == post_layover_dict['airport']
    assert layover.timedelta().total_seconds() == post_layover_dict['time']
    assert layover.change_planes == post_layover_dict['change_planes']

    # Now pull the list from the site
    response = apiclient.get(layover_list)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.data[0].get('airport') == layover.airport.abrev
    assert response.data[0].get('timedelta') == layover.timedelta()
    assert response.data[0].get('change_planes') == layover.change_planes

@pytest.mark.django_db
@pytest.mark.parametrize('kwargs',[
    {'airport':'BBB'},
])
def test_post_bad_keys(apiclient,layover_list,post_layover_dict,kwargs):
    post_layover_dict.update(kwargs)
    response = apiclient.post(layover_list,post_layover_dict)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert list(kwargs.keys())[0] in str(response.json())
    assert "object does not exist" in str(response.json())


'''
Currently this isn't quite functioning yet.  I have the validators working
in the LayoverManager class, but in order to not have to pass the flights
explicitly and leverage the url from the view, the view has a serializer.save
override to include the flight.  This seems to be called after validate...so
I can't seem to find a way to get the validation to work here without adjusting
the url schema or explicitly passing the flight, which I don't want to do.
'''
# @pytest.mark.django_db
# @pytest.mark.parametrize('kwargs,error_bool',[
#     ({'time': -50},True),
# ])
# def test_post_bad_field(apiclient,layover_list,post_layover_dict,kwargs,error_bool):
#     post_layover_dict.update(kwargs)
#     response = apiclient.post(layover_list,post_layover_dict)
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#     assert list(kwargs.keys())[0] in str(response.json())

# TODO: Can't make this work just yet...
# @pytest.mark.django_db
# @pytest.mark.parametrize('airport',['ATL','BOI'])
# def test_post_bad_airport(apiclient,layover_list,post_layover_dict,airport):
#     post_layover_dict.update({'airport':airport})
#
#     response = apiclient.post(layover_list,post_layover_dict)
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#     assert airport in str(response.json())
