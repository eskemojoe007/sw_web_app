import pytest
from django.urls import reverse
from rest_framework import status
from query_flight.models import Airport
import pytz
# from .conftest import check_get, check_post


@pytest.fixture
def airport_list():
    return reverse('query_flight:airports-list')

@pytest.mark.django_db
def test_airport_list(apiclient,airport_list):
    response = apiclient.get(airport_list)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
@pytest.mark.parametrize('airports_dict',['ATL','BOI','DAL'],indirect=True)
def test_get_airports(apiclient,airport_list,airports_dict):
    response = apiclient.post(airport_list,airports_dict)
    assert response.status_code == status.HTTP_201_CREATED
    assert Airport.objects.count() == 1

    # Make sure it saved and put it self into the test db
    airport = Airport.objects.get()
    assert airport.title == airports_dict['title']
    assert airport.get_tz_obj().zone == airports_dict['timezone']
    assert airport.get_tz_obj() == pytz.timezone(airports_dict['timezone'])

    # Now pull the list from the site
    response = apiclient.get(airport_list)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.data[0].get('title') == airport.title
    assert response.data[0].get('abrev') == airport.abrev
    assert response.data[0].get('timezone') == airport.get_tz_obj().zone

    # Now get it individually
    response = apiclient.get(reverse('query_flight:airports-detail',args=[airport.abrev]))
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('title') == airport.title
    assert response.data.get('abrev') == airport.abrev
    assert response.data.get('timezone') == airport.get_tz_obj().zone

@pytest.mark.parametrize("kwargs,func",[
    ({'latitude':92.6407},'full_clean'),
    ({'latitude':92.6407},'save'),
    ({'latitude':92.6407,'country':'us','state':'GA'},'full_clean'),
    # # ({'latitude':92.6407,'country':'us','state':'GA'},'save'),
    ({'latitude':-92.6407},'full_clean'),
    ({'longitude':-184.4277},'save'),
    ({'longitude':184.4277},'save'),
    ({'latitude':89.99},'full_clean'),
    ({'latitude':89.99},'save'),
    ({'timezone':'US/BlahBlah'},'full_clean'),
    ({'timezone':'US/BlahBlah'},'save'),
])
def test_validators(self,kwargs,func,atl_dict):

    #Change the info in the atl_dict_dict and get the airport object
    atl_dict.update(kwargs)
    airport = get_airport(**atl_dict)

    #Only testing the validators...not the save
    with pytest.raises(ValidationError)  as excinfo:
        f = getattr(airport,func)
        f()
