from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
# from django.core.validators import EmailValidator
from miktel.models import *
from miktel.choices_field import *


class FilterForm(forms.Form):
    shops = forms.ModelChoiceField(
        label="Wybierz salon/magazyn",
        queryset=Sklep.objects.filter(serwis_zew=False),
        required=False)
    mark = forms.ModelChoiceField(label="Wybierz marke/producent",
                                  queryset=Marka.objects.filter(gsm=True),
                                  required=False)
    category = forms.ModelChoiceField(label="Wybierz kategorię/typ",
                                      queryset=Kategoria.objects.all(),
                                      required=False)
    price_start = forms.IntegerField(
        label="Cena od",
        min_value=0,
        max_value=10000,
        required=False,
    )
    price_end = forms.IntegerField(
        label="Cena do",
        min_value=0,
        max_value=10000,
        required=False,
    )
    promo = forms.BooleanField(label="Promocja", required=False)


class FilterSerwisForm(forms.Form):
    shops = forms.ModelChoiceField(
        label="Wybierz salon/magazyn",
        queryset=Sklep.objects.filter(serwis_zew=False),
        required=False)
    mark = forms.ModelChoiceField(label="Wybierz marke/producent",
                                  queryset=Marka.objects.filter(gsm=True),
                                  required=False)
    typ = forms.ModelChoiceField(label="Wybierz typ części",
                                 queryset=Typ.objects.all(),
                                 required=False)
    promo = forms.BooleanField(label="Promocja", required=False)


from django.conf import settings
from captcha.fields import ReCaptchaField


class ReCAPTCHAForm(forms.Form):
    captcha = ReCaptchaField()