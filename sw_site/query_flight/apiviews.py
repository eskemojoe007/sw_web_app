# from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import AirportSerializer
from .models import Airport,Flight,Layover

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
