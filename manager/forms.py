from django import forms
from index.models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class DateRange(forms.Form):
    startDate = forms.DateField(widget=DateInput, label='Начало')
    endDate = forms.DateField(widget=DateInput, label='Конец')

    # class Meta:
    #     model = Request
    #     fields = ('data',)