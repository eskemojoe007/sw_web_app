# from rest_framework.views import APIView
from rest_framework import viewsets, generics
# from .serializers import AirportSerializer, FlightSerializer, LayoverSerializer
from . import serializers
from .models import Airport,Flight,Layover,Search


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = serializers.AirportSerializer

class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = serializers.SearchSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    # serializer_class = serializers.FlightSerializer
    def get_serializer_class(self):
        if self.action in ['list','retreive']:
            return serializers.FlightGetSerializer
        if self.action == 'create':
            return serializers.FlightPostSerializer
        return serializers.FlightGetSerializer

class LayoverList(generics.ListCreateAPIView):
    serializer_class = serializers.LayoverSerializer

    def get_queryset(self):
        return Layover.objects.filter(flight_id=self.kwargs["pk"])

    def perform_create(self,serializer):
        serializer.save(flight=Flight.objects.get(pk=self.kwargs['pk']))

    # def post(self, request, *args, **kwargs):
    #     flight = Flight.objects.get(pk=self.kwargs['pk'])
    #     print(repr(request))
    #     print(self.kwargs)
    #     print(kwargs)
    #     return super().post(request,*args,**kwargs)
