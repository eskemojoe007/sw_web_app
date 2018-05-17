# from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import AirportSerializer, FlightSerializer
from .models import Airport,Flight,Layover

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
