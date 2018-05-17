from rest_framework import serializers
from .models import Airport, Flight, Layover

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = (
            'title',
            'abrev',
            'latitude',
            'longitude',
            'sw_airport',
            'country',
            'state',
        )
