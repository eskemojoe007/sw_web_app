from rest_framework import serializers
from .models import Airport, Flight, Layover, Search, SearchCard, SearchCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import pytz
import six
from .utils import SW_Sel_Single
import itertools
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
        '''
        By default we don't need country or state...here we make you need it
        This is similar to model code, but needs to be added here as to
        trigger 400 errors and some other basic validation
        '''

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


class SearchCardPostSerializer(serializers.Serializer):
    destinationAirportCodes = AirportListField()
    originationAirportCodes = AirportListField()
    dates = DateListField()
    search_card = SearchCardGetSerializer(read_only=True)

    class SearchCardTemp(object):
        def __init__(
            self, destinationAirportCodes,
            originationAirportCodes, dates, search_card, search_cases
        ):
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
        for case in raw_cases:
            SearchCase.objects.create(search_card=sc,
                                      date=case[2],
                                      origin_airport=Airport.objects.get(
                                          pk=case[1]),
                                      destination_airport=Airport.objects.get(pk=case[0]))

        return self.SearchCardTemp(
            destinationAirportCodes, originationAirportCodes,
            dates, sc, sc.searchcase_set
        )

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


class SearchPostSerializer(serializers.Serializer):
    destinationAirportCode = serializers.CharField(max_length=4)
    originationAirportCode = serializers.CharField(max_length=4)
    departureDate = serializers.DateField()
    # returnDate = serializers.DateField()

    def create(self, validated_data):
        sw = SW_Sel_Single(departureDate=validated_data['departureDate'],
                           destinationAirportCode=validated_data['destinationAirportCode'],
                           originationAirportCode=validated_data['originationAirportCode'])
        # originationAirportCode=validated_data['originationAirportCode'],
        # returnDate=validated_data['returnDate'])
        sw.save_all_flights()
        sw.browser.quit()
        return sw

    def validate_destinationAirportCode(self, value):
        return self._check_airport(value)

    def validate_originationAirportCode(self, value):
        return self._check_airport(value)

    def _check_airport(self, code):
        if not Airport.objects.filter(abrev__iexact=code).exists():
            raise ValidationError(_(
                'Specified Airport is not valid: %(key)s'),
                params={'key': code}, code='bad_airport')
            return code
        else:
            return Airport.objects.get(abrev__iexact=code).abrev

    def validate_departureDate(self, value):
        self._check_date_past(value)
        return value

    # def validate_returnDate(self,value):
    #     self._check_date_past(value)
    #     return value

    # def _check_date_past(self, input_date):
    #     n = timezone.now().date()
    #     if input_date < n:
    #         raise ValidationError(_('Invalid date - date is in the past: current date - %(now)s, your date - %(your)s'),
    #                               params={'now': n, 'your': input_date}, code='past_date')

    # def validate(self,attrs):
    #     if attrs['returnDate'] < attrs['departureDate']:
    #         raise ValidationError(_(
    #             'Invalid date - return must be after departure: return date - %(ret)s, departur date - %(dep)s'),
    #             params={'ret':attrs['returnDate'],'dep':attrs['departureDate']},
    #             code='bad_date')
    #     return attrs
