import pytest
from query_flight import utils
from query_flight.models import Search, Flight, Layover, Airport
from django.utils import timezone


# @pytest.fixture
# def basic_search():
#     return Search.objects.create()

@pytest.fixture
def basic_sw_inputs():
    return {'browser':1,'originationAirportCode':['ATL','DAL'],
        'destinationAirportCode':'DEN',
        'departureDate':timezone.now().date()}


@pytest.mark.django_db
@pytest.mark.parametrize('input,iterable',[
    (['ATL','BOI','DEN'],True),
    ([1,2,3],True),
    ((1,2,3),True),
    ('string of garbage',False),
    (b'string of garbage',False),
    (1,False),
])
def test_check_iterable(input,iterable,basic_sw_inputs):
    assert utils.SW_Sel_base(**basic_sw_inputs)._check_iterable(input) == iterable

@pytest.mark.django_db
def test_create_search1(basic_sw_inputs):
    search = Search.objects.create()

    basic_sw_inputs.update({'search':search})

    s = utils.SW_Sel_base(**basic_sw_inputs)

    assert s.search is search
    assert s.search.id == search.id

@pytest.mark.django_db
def test_create_search2(basic_sw_inputs):
    s = utils.SW_Sel_base(**basic_sw_inputs)
    assert isinstance(s.search,Search)
    assert Search.objects.count() == 1

@pytest.mark.django_db
def test_create_search3(basic_sw_inputs):
    basic_sw_inputs.update({'search':1})
    with pytest.raises(ValueError):
        s = utils.SW_Sel_base(**basic_sw_inputs)

@pytest.mark.django_db
def test_cases(basic_sw_inputs):
    s = utils.SW_Sel_Multiple(**basic_sw_inputs)

    assert s.cases[0] == {'departureDate': timezone.now().date(),
        'destinationAirportCode': 'DEN',
        'originationAirportCode': 'ATL'}

    assert s.cases[1] == {'departureDate': timezone.now().date(),
        'destinationAirportCode': 'DEN',
        'originationAirportCode': 'DAL'}
