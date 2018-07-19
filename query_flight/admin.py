from django.contrib import admin
from .models import Airport, Flight, Layover
from django.utils.translation import gettext_lazy as _

# THis is a custom class used to change the tags for the filter for the airport


class SW_Filter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Southwest Airport')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'sw_airport'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('SW_Only', _('SW Airports Only')),
            ('Non_SW', _('Non SW Airports')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # super().queryset(args)
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        # if self.value() is 'All':
        #     return queryset

        if self.value() == 'SW_Only':
            return queryset.filter(sw_airport=True)

        if self.value() == 'Non_SW':
            return queryset.filter(sw_airport=False)

    # def value(self):
    #     value = super().value()
    #     if value is None:
    #         value = 'SW_Only'
    #     return str(value)


class LayoverInline(admin.TabularInline):
    model = Layover


class AirportAdmin(admin.ModelAdmin):
    # fields = ['pub_date','question_text']
    fieldsets = [
        ('Title', {'fields': ['title', 'abrev', 'sw_airport']}),
        ('Location Information', {'fields': [
         'timezone', 'latitude', 'longitude']}),
        ('Optional Location Data', {'fields': [
         'country', 'state'], 'classes': ['collapse in', ]})
    ]
    list_display = ('__str__', 'sw_airport', 'state', 'country')

    list_filter = [SW_Filter, ]
    # list_filter = ['sw_airport']
    search_fields = ['title', 'abrev']


admin.site.register(Airport, AirportAdmin)


class FlightAdmin(admin.ModelAdmin):
    # fields = ['pub_date','question_text']
    list_display = ('pk', 'origin_airport', 'destination_airport',
                    'travel_time', 'min_price', 'num_layovers')
    inlines = [LayoverInline]

    # list_filter = ['sw_airport']


admin.site.register(Flight, FlightAdmin)


class LayoverAdmin(admin.ModelAdmin):
    # fields = ['pub_date','question_text']
    list_display = ('airport', 'timedelta', 'change_planes')

    # list_filter = ['sw_airport']


admin.site.register(Layover, LayoverAdmin)
