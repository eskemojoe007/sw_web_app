# from rest_framework.views import APIView
from rest_framework import viewsets, generics
from .serializers import AirportSerializer, FlightSerializer, LayoverSerializer
from .models import Airport,Flight,Layover


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class LayoverList(generics.ListCreateAPIView):
    serializer_class = LayoverSerializer

    def get_queryset(self):
        return Layover.objects.filter(flight_id=self.kwargs["pk"])
