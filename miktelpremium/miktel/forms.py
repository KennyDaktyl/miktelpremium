from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from miktel.models import *

# from djang1o.views.generic.edit \
#     import CreateView
# from django.urls import reverse_lazy
# from .models import *

# tab_marka = []
# marka = Marka.objects.all()
# for el in marka:
#     tab_marka.append(el.nazwa)

tab_marka = [("1", "Apple"), ("2", "Sony")]


class UmowaKomisowaForm(forms.Form):
    # marka = forms.ModelChoiceField(queryset=Marka.objects.all())
    phones = forms.ModelChoiceField(
        label="Telefon", queryset=Telefon.objects.filter(dokument=False))
    # nazwa = forms.CharField(label='Nazwa modelu', max_length=64)
    komitent = forms.CharField(label="Imię i nazwisko komitenta",
                               max_length=128)
    adres_komitenta = forms.CharField(label="Zamieszkały", max_length=128)
    numer_dowodu = forms.CharField(label="Numer dowodu",
                                   min_length=3,
                                   max_length=9)


class FakturaZakupuForm(forms.Form):
    numer = forms.CharField(label="Numer faktury",
                            min_length=3,
                            max_length=128)
    hurtownia = forms.ModelChoiceField(label="Hurtownia",
                                       queryset=Hurtownia.objects.all())
    telefon = forms.ModelMultipleChoiceField(
        label="Dodaj telefony",
        queryset=Telefon.objects.filter(dokument=False))


class TelefonCreateForm(forms.ModelForm):
    class Meta:
        model = Telefon
        exclude = ("sklep", "dostepny", "dokument", "zdjecia",
                   "pracownik_sprzed", 'pracownik_zak', 'sklep_sprzed')
        help_texts = {
            "imei": "wpisz minimum 4 ostatnich cyfr",
            "cena_zak": "wpisz cenę Brutto jeśli kupujesz na Vat",
        }


class GetServiceForm(forms.Form):
    usluga = forms.ModelChoiceField(
        label="Usługa",
        queryset=Usluga.objects.filter(sprzedaz=False).filter(
            zakup=False).filter(grawer=False),
    )
    model = forms.CharField(label="Nazwa modelu", min_length=3, max_length=128)
    imei = forms.CharField(min_length=4, max_length=14)
    cena_zgoda = forms.IntegerField(label="Wstępna wycena naprawy",
                                    min_value=0,
                                    max_value=10000)
    numer_telefonu = forms.CharField(label="Numer telefonu do klienta",
                                     min_length=9,
                                     max_length=14)
    imie_nazwisko = forms.CharField(label="Dane klienta",
                                    min_length=5,
                                    max_length=14)
    info = forms.CharField(required=False,
                           label="Dodatkowe informacje",
                           max_length=256)


class ServiceReadyForm(forms.Form):
    cena_zgoda = forms.IntegerField(label="Ostateczna cena za naprawę",
                                    min_value=0,
                                    max_value=1000)
    koszt = forms.IntegerField(required=False,
                               label="Koszty seriwsu",
                               min_value=0,
                               max_value=1000)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class UmowaKomisuForm(ModelForm):
    # telefon_id = forms.ModelMultipleChoiceField(label='Dodaj telefony',
    #                                             queryset=Telefon.objects.filter(dokument=False))

    class Meta:
        model = UmowaKomisowaNew
        fields = ["komitent", "adres_komitenta", "numer_dowodu", "phones"]


class CzescCreateForm(forms.Form):
    foto = forms.ModelMultipleChoiceField(required=False,
                                          label="Dodaj zdjęcia",
                                          queryset=Foto.objects.filter(used=False))
    typ = forms.ModelChoiceField(label="Typ części",
                                 queryset=Typ.objects.all())
    marka = forms.ModelChoiceField(label="Marka",
                                   queryset=Marka.objects.all())
    stan = forms.ChoiceField(choices=StanCzesci, label="Stan części",
                             initial='0', widget=forms.Select(), required=True)
    kolor = forms.ChoiceField(choices=Kolor, label="Kolor części",
                              initial='0', widget=forms.Select(), required=True)
    nazwa = forms.CharField(label="Nazwa modelu",
                            min_length=1,
                            max_length=30)
    cena_zak = forms.IntegerField(label="Cena zakupu",
                                  min_value=0,
                                  max_value=10000)
    cena_sprzed = forms.IntegerField(label="Cena sprzedaży",
                                     min_value=0,
                                     max_value=10000)
    ilosc = forms.IntegerField(label="Ilość",
                               min_value=0,
                               max_value=10000)
    opis = forms.CharField(label="Opis części", max_length=300)

    #     def __init__(self, *args, **kwargs):
    #         dokument = kwargs.pop('dokument')
    #         super(UmowaKomisowaForm, self).__init__(*args, **kwargs)
    #         self.fields['telefon_id'].queryset = UmowaKomisowaNew.objects.filter(
    #             dokument=False)
    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user')
    #     super(UmowaKomisuForm, self).__init__(self, *args, **kwargs)
    #     self.fields['phones'].queryset = UmowaKomisowaNew.objects.filter(
    #         user=user)


# class SesjaForm(forms.Form):
#     sklepy_praca = forms.ModelChoiceField(label='Wybierz dzisiejsze miejsce pracy',
#                                           queryset=Sklep.objects.all())
