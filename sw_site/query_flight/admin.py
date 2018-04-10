from django.contrib import admin
from .models import Airport

# Register your models here.
class AirportAdmin(admin.ModelAdmin):
    # fields = ['pub_date','question_text']
    fieldsets = [
    ('Title', {'fields':['title','abrev','sw_airport']}),
    ('Location Information', {'fields':['timezone','lattitude','longitude']})
    ]
    list_display = ('__str__', 'sw_airport','get_state')
    list_filter = ['sw_airport']
    search_fields = ['title']
admin.site.register(Airport,AirportAdmin)
