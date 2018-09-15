from rest_framework import serializers
from .models import Airport, Flight, Layover, Search, SearchCard, SearchCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import pytz
import six
# from .utils import SW_Sel_Single
import itertools
from rest_framework.reverse import reverse
# import itertools


class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError(_('Unknown timezone'),
                                  code='unknown Timezone')


class AirportSerializer(serializers.ModelSerializer):
    # country = serializers.CharField(required=False)
    timezone = TimezoneField()

    class Meta:
        model = Airport
        fields = ('__all__')

    def validate(self, attrs):
        """Validate input values.

        By default we don't need country or state...here we make you need it
        This is similar to model code, but needs to be added here as to
        trigger 400 errors and some other basic validation
        """

        if not attrs.get('country'):
            airport = Airport.objects.lookup_missing(**attrs)
            attrs.update({'country': airport.country})

            if airport.state:
                attrs.update({'state': airport.state})
        # raise ValidationError(_('Need to specify country on serializer'),code='no country')
        return attrs


class LayoverSerializer(serializers.ModelSerializer):
    airport = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Airport.objects.all())
    # flight = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Layover
        fields = ('airport', 'change_planes', 'timedelta', 'time')
        extra_kwargs = {'time': {'write_only': True}}

    # def validate(self, attrs):
    #     '''want to run the checks in the manager'''
    #     layover = Layover.objects.validate_layover(**attrs)
    #     return attrs


class FlightGetSerializer(serializers.ModelSerializer):
    # origin_airport = AirportSerializer(read_only=True,required=False)
    # destination_airport = AirportSerializer(read_only=True,required=False)
    layover_set = LayoverSerializer(read_only=True, many=True, required=False)

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
        read_only_fields = ('id', 'travel_time', 'min_price',)


class FlightPostSerializer(serializers.ModelSerializer):
    # origin_airport = AirportPKSerializer(read_only=False,required=True)
    # destination_airport = AirportSerializer(read_only=False,required=True)
    origin_airport = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Airport.objects.all())
    destination_airport = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Airport.objects.all())
    search = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Search.objects.all())
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

    # TODO: Create the search if it doesn't exist yet...we may want to do that
    # since its so simple.
    # def create(self,validated_data):
    #     pass

    def validate(self, attrs):
        '''want to run the checks in the manager'''
        Flight.objects.validate_flight(**attrs)
        return attrs

# class ValidateAirportCodeMixins(object):


# class AirportListField(serializers.ListField):
#     child = serializers.CharField(max_length=4)


class SearchCardGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchCard
        fields = (
            'id',
            'search',
            'num_flights',
            'origins',
            'destinations',
            'dates',
            'num_cases',
        )


class SearchSerializer(serializers.ModelSerializer):
    searchcard_set = SearchCardGetSerializer(read_only=True, many=True)
    # flight_set = FlightGetSerializer(read_only=True, many=True, required=False)

    class Meta:
        model = Search
        fields = ('id', 'submitted', 'started', 'completed', 'total_time',
                  'num_cards', 'searchcard_set')
        read_only_fields = ('submitted', 'total_time', 'num_cards')


class AirportListField(serializers.ListField):
    child = serializers.CharField(max_length=4)


class DateListField(serializers.ListField):
    child = serializers.DateField()


class SearchCardGenericPostSerializer(serializers.Serializer):
    destinationAirportCodes = AirportListField()
    originationAirportCodes = AirportListField()
    dates = DateListField()

    def validate_destinationAirportCodes(self, value):
        return self._check_airports(value)

    def validate_originationAirportCodes(self, value):
        return self._check_airports(value)

    def validate_dates(self, value):
        if self._duplicates(value):
            raise ValidationError(_(
                'Duplicated input dates: %(key)s'),
                params={'key': value}, code='duplicate_dates')

        n = timezone.now().date()
        for date in value:
            if date < n:
                raise ValidationError(_(
                    'Invalid date - date is in the past: current date - %(now)s, your date - %(your)s'),
                    params={'now': n, 'your': date}, code='past_date')
        return value

    def _check_airports(self, code_list):
        clean_codes = []
        for code in code_list:
            clean_codes.append(self._check_airport(code))

        if self._duplicates(code_list):
            raise ValidationError(_(
                'Repeat airports in input %(key)s'),
                params={'key': clean_codes}, code='bad_airports')
        return clean_codes

    def _check_airport(self, code):
        if not Airport.objects.filter(abrev__iexact=code).exists():
            raise ValidationError(_(
                'Specified Airport is not valid: %(key)s'),
                params={'key': code}, code='bad_airport')
            return code
        else:
            return Airport.objects.get(abrev__iexact=code).abrev

    @staticmethod
    def _intersect(a, b):
        return not set(a).isdisjoint(b)

    @staticmethod
    def _duplicates(a):
        return len(a) != len(set(a))

    def validate(self, attrs):
        if self._intersect(attrs['destinationAirportCodes'],
                           attrs['originationAirportCodes']):
            raise ValidationError(_(
                'Cannot repeat airport in both destination and origin'),
                code='origin destination non-unique')
        return attrs


class SearchCardPostSerializer(SearchCardGenericPostSerializer):
    search_card = SearchCardGetSerializer(read_only=True)

    class SearchCardClass(object):
        """Basic temporary class for post return."""

        def __init__(
            self, destinationAirportCodes,
            originationAirportCodes, dates, search_card, search_cases
        ):
            """Set objects."""

            self.originationAirportCodes = originationAirportCodes
            self.destinationAirportCodes = destinationAirportCodes
            self.dates = dates
            self.search_card = search_card
            self.search_cases = search_cases

    def create(self, validated_data):
        destinationAirportCodes = validated_data['destinationAirportCodes']
        originationAirportCodes = validated_data['originationAirportCodes']
        dates = validated_data['dates']

        sc = SearchCard.objects.create()

        s = [field for field in [destinationAirportCodes,
                                 originationAirportCodes, dates]]
        raw_cases = itertools.product(*s)
        for dest, origin, date in raw_cases:
            SearchCase.objects.create(search_card=sc,
                                      date=date,
                                      origin_airport=Airport.objects.get(
                                          pk=origin),
                                      destination_airport=Airport.objects.get(pk=dest))

        return self.SearchCardClass(
            destinationAirportCodes, originationAirportCodes,
            dates, sc, sc.searchcase_set
        )


class SearchPostSerializer(serializers.Serializer):
    cards = SearchCardGenericPostSerializer(many=True, required=True)
    search_id = serializers.IntegerField(read_only=True)
    search_url = serializers.CharField(read_only=True)
    # search = SearchSerializer(read_only=True)
    # TODO: Make the search optional input to update existing searches.
    # we may need to make significant model updates to accmplish however (like start)
    # Stop etc times...those could be an attached model.
    # search = serializers.PrimaryKeyRelatedField(
    #     read_only=False, queryset=Airport.objects.all(), required=False)

    class SearchClass(object):
        """Basic temporary class for post return."""

        def __init__(self, search_id, search_url):
            """Set objects."""

            self.search_id = search_id
            self.search_url = search_url
            # self.cards = cards
            # self.celery_url = celery_url

    def create(self, validated_data):
        search = Search.objects.create()

        return self.SearchClass(
            search.id,
            reverse('query_flight:searchs-detail', args=[search.id]))
