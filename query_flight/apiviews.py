# from rest_framework.views import APIView
from rest_framework import viewsets, generics, mixins
# from .serializers import AirportSerializer, FlightSerializer, LayoverSerializer
from . import serializers
from .models import Airport, Flight, Layover, Search, SearchCard
from rest_framework.response import Response
from rest_framework import status



class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = serializers.AirportSerializer


class SearchViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Search.objects.all()
    serializer_class = serializers.SearchSerializer


class SearchCardViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = SearchCard.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retreive']:
            return serializers.SearchCardGetSerializer
        if self.action == 'create':
            return serializers.SearchCardPostSerializer
        return serializers.SearchCardGetSerializer

    def create(self, request, *args, **kwargs):
        print(self.action)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    # serializer_class = serializers.FlightSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retreive']:
            return serializers.FlightGetSerializer
        if self.action == 'create':
            return serializers.FlightPostSerializer
        return serializers.FlightGetSerializer


class LayoverList(generics.ListCreateAPIView):
    serializer_class = serializers.LayoverSerializer

    def get_queryset(self):
        return Layover.objects.filter(flight_id=self.kwargs["pk"])

    def perform_create(self, serializer):
        serializer.save(flight=Flight.objects.get(pk=self.kwargs['pk']))


class SearchPost(generics.CreateAPIView):
    serializer_class = serializers.SearchPostSerializer
