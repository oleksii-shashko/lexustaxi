from django import forms
from django.apps import apps
Request = apps.get_model("index", "Request")
Car = apps.get_model("index", "Car")
Address = apps.get_model("index", "Address")


class Order(forms.Form):
    car = forms.ModelChoiceField(Car.objects.all(), label="Класс такси",
                                 widget=forms.Select(
                                     attrs={
                                         "class": "form-control"
                                     }
                                 ))
    _from = forms.ModelChoiceField(Address.objects.all(), label="Откуда",
                                   widget=forms.Select(
                                       attrs={
                                           "class": "form-control"
                                       }
                                   ))
    _to = forms.ModelChoiceField(Address.objects.all(), label="Куда",
                                 widget=forms.Select(
                                     attrs={
                                         "class": "form-control"
                                     }
                                 ))
    comment = forms.CharField(label="Комментарий",
                              required=False,
                              widget=forms.Textarea(
                                  attrs={
                                      "rows": "5",
                                      "class": "form-control"
                                  }
                              ))

    def clean(self):
        if not self.cleaned_data.get("car") or not self.cleaned_data.get("_from") or not self.cleaned_data.get("_to"):
            raise forms.ValidationError("Wrong input!")
