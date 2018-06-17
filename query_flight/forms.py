from django import forms
from .models import Flight, Airport
from django.contrib.admin.widgets import AdminDateWidget
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ('origin_airport', 'destination_airport', 'depart_time',
                  'arrive_time', 'wanna_get_away', 'anytime',
                  'business_select',)


class SearchForm(forms.Form):
    origin_airport = forms.ModelMultipleChoiceField(Airport.objects.filter(
        sw_airport=True),
        label='Origin Airports',
        widget=forms.CheckboxSelectMultiple)
    destination_airport = forms.ModelMultipleChoiceField(Airport.objects.filter(
        sw_airport=True),
        label='Destination Airports',
        widget=forms.CheckboxSelectMultiple)
    depart_date = forms.DateField(
        label='Departure Date',
        widget=forms.TextInput(attrs={'class': 'datepicker'}))
    # return_date = forms.DateField(label='Return Date',widget=forms.TextInput(attrs={'class':'datepicker'}))

    def clean_depart_date(self):
        data = self.cleaned_data['depart_date']
        self._check_date_past(data)
        return data

    # def clean_return_date(self):
    #     data = self.cleaned_data['return_date']
    #     self._check_date_past(data)
    #     # depart = self.cleaned_data['depart_date']
    #     # if data < depart:
    #     #     raise ValidationError(_('Invalid date - return date (%(return)s) must be after depart date(%(depart)s)'),
    #     #     params={'return':data,'depart':depart},code='return_depart_date')
    #     return data

    def _check_date_past(self, input_date):
        n = timezone.now().date()
        if input_date < n:
            raise ValidationError(_('Invalid date - date is in the past: current date - %(now)s, your date - %(your)s'),
                                  params={'now': n, 'your': input_date}, code='past_date')

    # def clean(self):
    #     cleaned_data = super().clean()
    #     depart_date = cleaned_data.get('depart_date')
    #     return_date = cleaned_data.get('return_date')
    #
    #     if depart_date and return_date and (return_date < depart_date):
    #         msg = _('Return Date must be after Depart Date')
    #         self.add_error('depart_date',msg)
    #         self.add_error('return_date',msg)

    # def __init__(self,*args,**kwargs):
    #     # super().__init__(*args,**kwagrs)
    #     self.depart_date = timezone.now()
    #     self.return_date = timezone.now()
