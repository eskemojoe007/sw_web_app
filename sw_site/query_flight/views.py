from django.shortcuts import render
from django.http import HttpResponse
from .models import Airport, Flight
from django.shortcuts import get_object_or_404, render


def index(request):
    return HttpResponse("Hello, world. You're at the Query Flight index.")


def airport(request,airport_id):
    airport = get_object_or_404(Airport,pk=airport_id.upper())
    return render(request,'query_flight/airport.html',{'airport':airport})
