from rest_framework import serializers
from .models import Airport, Flight, Layover
from django.core.exceptions import ValidationError
import pytz
import six

class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')

class AirportSerializer(serializers.ModelSerializer):
    timezone = TimezoneField()
    class Meta:
        model = Airport
        fields = ('__all__')

class LayoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layover
        fields = ('airport','change_planes','get_timedelta','time')
        extra_kwargs = {'time':{'write_only':True}}

class FlightSerializer(serializers.ModelSerializer):
    origin_airport = AirportSerializer(read_only=True,required=False)
    destination_airport = AirportSerializer(read_only=True,required=False)
    layover_set = LayoverSerializer(read_only=True,many=True,required=False)
    class Meta:
        model = Flight
        fields = (
            'id',
            'origin_airport',
            'destination_airport',
            'depart_time',
            'arrive_time',
            'wanna_get_away',
            'anytime',
            'business_select',
            'travel_time',
            'min_price',
            'layover_set',
        )
        read_only_fields = ('id','travel_time','min_price',)
