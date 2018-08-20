# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Airport
# from .models import Flight
# from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import generic
from .forms import SearchForm
# from .forms import FlightForm, SearchForm
from django.urls import reverse
from .utils import SW_Sel_Multiple
from .tasks import add


def index(request):
    return render(request, 'query_flight/index.html')
    # return HttpResponse("Hello, world. You're at the Query Flight index.")


# def flight_new(request):
#     form = FlightForm()
#     return render(request, 'query_flight/flight.html', {'form': form})


def dummy(request):
    # if request.method == 'POST':
    #
    #     # create a form instance and populate it with data from the request:
    #     form = SearchForm(request.POST)
    #
        # add.delay(4, 4)
    #     return HttpResponse('You called DUMMY!')
    # else:
    #     form = SearchForm()
    # return render(request, 'query_flight/search.html', {'form': form})
    add.delay(4, 4)
    return HttpResponse('You called DUMMY!')


def search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            originationAirportCode = form.cleaned_data['origin_airport'].values_list(
                'abrev', flat=True)
            destinationAirportCode = form.cleaned_data['destination_airport'].values_list(
                'abrev', flat=True)
            departureDate = form.cleaned_data['depart_date'].strftime(
                '%Y-%m-%d')
            # returnDate = form.cleaned_data['return_date'].strftime('%Y-%m-%d')

            sw = SW_Sel_Multiple(departureDate=departureDate,
                                 destinationAirportCode=destinationAirportCode,
                                 originationAirportCode=originationAirportCode)
            # returnDate=returnDate)
            sw.save_all_flights()
            sw.browser.quit()
            return HttpResponseRedirect(reverse('query_flight:searchs-detail', args=[sw.search.id]))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'query_flight/search.html', {'form': form})


class AirportIndexView(generic.ListView):
    template_name = 'query_flight/airportindex.html'
    context_object_name = 'airport_list'

    def get_queryset(self):
        return Airport.objects.filter(sw_airport=True).order_by('abrev')

# def airport(request,airport_id):
#     airport = get_object_or_404(Airport,pk=airport_id.upper())
#     return render(request,'query_flight/airport.html',{'airport':airport})


class AirportView(generic.DetailView):
    model = Airport
    template_name = 'query_flight/airport.html'
