from rest_framework import serializers
from .models import Airport, Flight, Layover, Search
# from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import pytz
import six

class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise serializers.ValidationError(_('Unknown timezone'),code='unknown Timezone')


class AirportSerializer(serializers.ModelSerializer):
    # country = serializers.CharField(required=False)
    timezone = TimezoneField()
    class Meta:
        model = Airport
        fields = ('__all__')
    def validate(self, attrs):
        # By default we don't need country or state...here we make you need it
        # This is similar to model code, but needs to be added here as to trigger
        # 400 errors and some other basic validation

        if not attrs.get('country'):
            airport = Airport.objects.lookup_missing(**attrs)
            attrs.update({'country':airport.country})

            if airport.state:
                attrs.update({'state':airport.state})
        # raise serializers.ValidationError(_('Need to specify country on serializer'),code='no country')
        return attrs

class LayoverSerializer(serializers.ModelSerializer):
    airport = serializers.PrimaryKeyRelatedField(read_only=False,queryset=Airport.objects.all())
    # flight = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Layover
        fields = ('airport','change_planes','timedelta','time')
        extra_kwargs = {'time':{'write_only':True}}

    # def validate(self, attrs):
    #     '''want to run the checks in the manager'''
    #     layover = Layover.objects.validate_layover(**attrs)
    #     return attrs


class FlightGetSerializer(serializers.ModelSerializer):
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

class SearchSerializer(serializers.ModelSerializer):
    flight_set = FlightGetSerializer(read_only=True,many=True,required=False)
    class Meta:
        model = Search
        fields = ('id','time','num_flights','flight_set')
        # read_only_fields = ('time','num_flights')

# class AirportPKSerializer(serializers.PrimaryKeyRelatedField):
#     def get_queryset(self):
#         return Airport.objects.all()

class FlightPostSerializer(serializers.ModelSerializer):
    # origin_airport = AirportPKSerializer(read_only=False,required=True)
    # destination_airport = AirportSerializer(read_only=False,required=True)
    origin_airport = serializers.PrimaryKeyRelatedField(read_only=False,queryset=Airport.objects.all())
    destination_airport = serializers.PrimaryKeyRelatedField(read_only=False,queryset=Airport.objects.all())
    search = serializers.PrimaryKeyRelatedField(read_only=False,queryset=Search.objects.all())
    # destination_airport = serializers.PrimaryKeyRelatedField(read_only=False)
    # search = serializers.PrimaryKeyRelatedField(read_only=False)
    class Meta:
        model = Flight
        fields = (
            'origin_airport',
            'destination_airport',
            'depart_time',
            'arrive_time',
            'wanna_get_away',
            'anytime',
            'business_select',
            'search',
        )

    ## TODO: Create the search if it doesn't exist yet...we may want to do that
    # since its so simple.
    # def create(self,validated_data):
    #     pass

    def validate(self, attrs):
        '''want to run the checks in the manager'''
        flight = Flight.objects.validate_flight(**attrs)
        return attrs
