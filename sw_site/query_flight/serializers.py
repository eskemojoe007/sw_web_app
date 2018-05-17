from rest_framework import serializers
from .models import Airport, Flight, Layover
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
