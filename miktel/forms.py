from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from miktel.models import *
from miktel.choices_field import *
from django.contrib.admin import widgets
from django.utils.dates import MONTHS

# from djang1o.views.generic.edit \
#     import CreateView
# from django.urls import reverse_lazy
# from .models import *

# tab_marka = []
# marka = Marka.objects.all()
# for el in marka:
#     tab_marka.append(el.nazwa)

tab_marka = [("1", "Apple"), ("2", "Sony")]


class UstawFotoForm(forms.ModelForm):
    class Meta:
        model = Foto
        exclude = ['used']


class UstawHasloForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = MyUser
        fields = ['password']


class PageRecordsForm(forms.Form):
    page_records = forms.ChoiceField(choices=IloscRekordow,
                                     label="Ustaw ilość rekordów na stronie",
                                     widget=forms.Select(),
                                     required=True,
                                     help_text='*')


class UmowaKomisowaForm(forms.Form):
    # marka = forms.ModelChoiceField(queryset=Marka.objects.all())
    phones = forms.ModelChoiceField(
        label="Telefon",
        queryset=Telefon.objects.filter(dokument=False).filter(dostepny=True))
    # nazwa = forms.CharField(label='Nazwa modelu', max_length=64)
    komitent = forms.CharField(label="Imię i nazwisko komitenta",
                               max_length=128)
    adres_komitenta = forms.CharField(label="Zamieszkały",
                                      max_length=128,
                                      required=False)
    numer_dowodu = forms.CharField(label="Numer dowodu",
                                   min_length=3,
                                   max_length=9)


class FakturaZakupuForm(forms.Form):
    numer = forms.CharField(label="Numer faktury", min_length=3, max_length=64)
    hurtownia = forms.ModelChoiceField(label="Hurtownia",
                                       queryset=Hurtownia.objects.all())
    telefon = forms.ModelMultipleChoiceField(
        label="Dodaj telefony",
        queryset=Telefon.objects.filter(dokument=False))


class TelefonCreateForm(forms.ModelForm):
    class Meta:
        model = Telefon
        exclude = ("sklep", "dostepny", "dokument", "zdjecia", "in_promo",
                   'slug', "foto", 'data_zmiany', "cena_promo",
                   "pracownik_sprzed", 'pracownik_zak', 'sklep_sprzed',
                   'zawieszony', 'data_wprow', 'data_sprzed', 'nr_doc',
                   'magazyn_aktualny')
        help_texts = {
            "imei": "wpisz minimum 4 ostatnich cyfr",
            "cena_zak": "wpisz cenę Brutto jeśli kupujesz na Vat",
        }
        # form = IngredienceForm()
        # form.fields["Marka"].queryset = Marka.objects.filter(gsm=True)


class GetServiceForm(forms.Form):
    usluga = forms.ModelChoiceField(
        label="Usługa",
        queryset=Usluga.objects.filter(sprzedaz=False).filter(
            zakup=False).filter(grawer=False).filter(akcesoria=False))
    marka = forms.ModelChoiceField(label="Marka",
                                   queryset=Marka.objects.filter(gsm=True))
    model = forms.CharField(label="Nazwa modelu",
                            min_length=2,
                            max_length=128,
                            help_text='*')
    imei = forms.CharField(min_length=4, max_length=15, help_text='*')
    cena_zgoda = forms.IntegerField(label="Wstępna wycena naprawy",
                                    min_value=0,
                                    max_value=10000,
                                    help_text='*')
    numer_telefonu = forms.CharField(label="Numer telefonu do klienta",
                                     min_length=9,
                                     max_length=9,
                                     required=False)
    imie_nazwisko = forms.CharField(label="Dane klienta",
                                    required=False,
                                    max_length=32)
    info = forms.CharField(required=False,
                           label="Dodatkowe informacje",
                           max_length=256)


class ServiceReadyForm(forms.Form):
    cena_zgoda = forms.IntegerField(label="Ostateczna cena za naprawę",
                                    min_value=0,
                                    max_value=1000,
                                    help_text='*')
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
    # foto = forms.ModelMultipleChoiceField(
    #     required=False,
    #     label="Dodaj zdjęcia",
    #     queryset=Foto.objects.filter(used=False))
    typ = forms.ModelChoiceField(label="Typ części",
                                 queryset=Typ.objects.all(),
                                 help_text='*')
    marka = forms.ModelChoiceField(label="Marka",
                                   queryset=Marka.objects.filter(gsm=True))
    stan = forms.ChoiceField(choices=StanCzesci,
                             label="Stan części",
                             initial='0',
                             widget=forms.Select(),
                             required=True,
                             help_text='*')
    kolor = forms.ChoiceField(choices=Kolor,
                              label="Kolor części",
                              initial='0',
                              widget=forms.Select(),
                              required=True,
                              help_text='*')
    nazwa = forms.CharField(label="Nazwa modelu",
                            min_length=1,
                            max_length=30,
                            help_text='*')
    cena_zak = forms.IntegerField(label="Cena zakupu",
                                  min_value=0,
                                  max_value=10000,
                                  help_text='*')
    cena_sprzed = forms.IntegerField(label="Cena sprzedaży",
                                     min_value=0,
                                     max_value=10000)
    ilosc = forms.IntegerField(label="Ilość",
                               min_value=0,
                               max_value=10000,
                               help_text='*')
    opis = forms.CharField(label="Opis części", max_length=300, required=False)


def cena_klient(value):
    if value < 1 or value > 10000:
        raise ValidationError("<b>Wypełnij pole cena klient</b>")


class CenaKlientForm(forms.Form):
    cena_klient = forms.IntegerField(label="Cena klient",
                                     min_value=0,
                                     max_value=10000,
                                     help_text="Cena od 0 do 10000",
                                     validators=[cena_klient])


class DodajWiecejCzesci(forms.Form):
    ilosc = forms.IntegerField(label="Ile sztuk dodajesz?",
                               min_value=1,
                               max_value=10,
                               help_text="Minimu 1 maximum 10")


class UsunWiecejCzesci(forms.Form):
    ilosc = forms.IntegerField(label="Ile sztuk usuwasz?",
                               min_value=1,
                               max_value=10,
                               help_text="Minimu 1 maximum 10")


class DodajWiecejCzesci_podbne(forms.Form):
    # foto = forms.ModelMultipleChoiceField(
    #     required=False,
    #     label="Dodaj zdjęcia",
    #     queryset=Foto.objects.filter(used=False))
    stan = forms.ChoiceField(choices=StanCzesci,
                             label="Stan części",
                             initial='0',
                             widget=forms.Select(),
                             required=True,
                             help_text='*')

    kolor = forms.ChoiceField(choices=Kolor,
                              label="Kolor części",
                              initial='0',
                              widget=forms.Select(),
                              required=True,
                              help_text='*')
    cena_zak = forms.IntegerField(label="Cena zakupu",
                                  min_value=0,
                                  max_value=10000,
                                  help_text='*')
    cena_sprzed = forms.IntegerField(label="Cena sprzedaży",
                                     min_value=0,
                                     max_value=10000,
                                     required=False)
    ilosc = forms.IntegerField(label="Ilość",
                               min_value=0,
                               max_value=10000,
                               help_text='*')
    opis = forms.CharField(label="Opis części", max_length=300, required=False)


class AddJobForm(forms.Form):
    model = forms.CharField(label="Nazwa modelu", min_length=3, max_length=128)
    cena_klient = forms.IntegerField(label="Cena klient",
                                     min_value=0,
                                     max_value=10000,
                                     help_text='*')
    koszt = forms.IntegerField(label="Koszt",
                               min_value=0,
                               max_value=10000,
                               help_text='*')


class InnePraceForm(forms.Form):
    nazwa = forms.CharField(label="Nazwa czynności",
                            min_length=3,
                            max_length=128,
                            help_text='*')
    czas = forms.IntegerField(label="Czas trwania",
                              min_value=0,
                              max_value=10000,
                              help_text='*')
    opis = forms.CharField(label="Opis usługi",
                           widget=forms.Textarea(),
                           max_length=300,
                           required=False,
                           help_text='*')


class DodajAkcesoriaForm(forms.Form):
    miesiac = forms.ChoiceField(choices=MIESIACE,
                                label="Wybierz miesiąc sprzedaży",
                                widget=forms.Select(),
                                required=True,
                                help_text='*')
    cena_klient = forms.IntegerField(label="Suma sprzedaży akcesoriów",
                                     min_value=0,
                                     max_value=100000,
                                     help_text='*')


class PhoneDetailsForm(forms.Form):
    color = forms.CharField(
        label="Kolor modelu",
        required=True,
        max_length=32,
    )
    foto_a = forms.CharField(
        label="Aparat tylni główny",
        required=True,
        max_length=32,
    )
    foto_b = forms.CharField(
        label="Aparat przedni",
        required=True,
        max_length=32,
    )
    battery = forms.CharField(
        label="Pojemność bateri",
        required=True,
        max_length=32,
    )
    system = forms.CharField(
        label="System operacyjny",
        required=True,
        max_length=32,
    )
    info = forms.CharField(
        label="Informacje inne",
        widget=forms.Textarea(),
        required=False,
        max_length=64,
    )
    image_mini = forms.FileField(required=False,
                                 label="Ustaw foto mini na listę telefonów")
    alt_mini = forms.CharField(
        label="Alternatywny tekst dla foto mini",
        required=False,
        max_length=64,
    )
    title_mini = forms.CharField(
        label="Tytuł zdjęcia dla foto mini",
        required=False,
        max_length=64,
    )


class ImagesForm(forms.Form):
    image_another = forms.FileField(
        label="Ustaw foto dodatkowego główne",
        required=True,
    )
    alt_another = forms.CharField(
        label="Alternatywny tekst dla foto dodatkowego głównego",
        required=False,
        max_length=64,
    )
    title_another = forms.CharField(
        label="Tytuł tekst dla foto dodatkowego głównego",
        required=True,
        max_length=64,
    )
    image_another_mini = forms.FileField(label="Ustaw foto dodatkowe mini",
                                         required=True)
    alt_another_mini = forms.CharField(
        label="Alternatywny tekst dla foto dodatkowego mini",
        required=True,
        max_length=64,
    )
    title_another_mini = forms.CharField(
        label="Tytuł zdjęcia dla foto dodatkowego mini",
        required=True,
        max_length=64,
    )
    # file_field = forms.FileField(widget=forms.ClearableFileInput(
    #     attrs={'multiple': True}))


class PaymentForm(forms.Form):
    hours_count = forms.IntegerField(label="Ilość godzin",
                                     min_value=1,
                                     initial=1,
                                     max_value=500,
                                     help_text='*')
    value = forms.IntegerField(label="Kwota",
                               min_value=0,
                               max_value=10000,
                               help_text='*')
    info = forms.CharField(
        label="Wpisz za jaki dni np 1(11h),2(11h),5(8h)",
        required=False,
        widget=forms.Textarea(),
        max_length=64,
    )


class PaymentAdvForm(forms.Form):

    value = forms.IntegerField(label="Kwota",
                               min_value=0,
                               max_value=10000,
                               help_text='*')
    info = forms.CharField(
        label="Wpisz info",
        required=False,
        widget=forms.Textarea(),
        max_length=64,
    )


month_choices = MONTHS.items()


class SetMonthForm(forms.Form):
    month = forms.ChoiceField(choices=month_choices,
                              label="Miesiąc",
                              initial=datetime.now().month,
                              widget=forms.Select(),
                              help_text="*",
                              required=False)


CHOICES = (
    (0, 'Wszystko'),
    (1, 'Wypłata'),
    (2, 'Zaliczka'),
    (3, 'Premia'),
)


class AdminPaymentsForm(forms.Form):
    user = forms.ModelChoiceField(
        label="Pracownik",
        queryset=MyUser.objects.filter(is_active=True),
        required=False)
    month = forms.ChoiceField(choices=month_choices,
                              label="Miesiąc",
                              initial=datetime.now().month,
                              widget=forms.Select(),
                              help_text="*",
                              required=False)
    type_payments = forms.ChoiceField(choices=CHOICES,
                                      label="Rodzaj wypłaty",
                                      widget=forms.Select(),
                                      initial=0,
                                      help_text="*",
                                      required=False)


YEARS = ((2020, '2020'), (2021, '2021'), (2022, '2022'), (2023, '2023'))


class SetNewSheduleForm(forms.Form):
    shop = forms.ModelChoiceField(
        label="Wybierz sklep",
        queryset=Sklep.objects.all(),
    )
    month = forms.ChoiceField(choices=month_choices,
                              label="Miesiąc",
                              initial=datetime.now().month,
                              widget=forms.Select(),
                              help_text="*",
                              required=False)
    year = forms.ChoiceField(choices=YEARS,
                             label="Rok",
                             initial=datetime.now().year,
                             widget=forms.Select(),
                             help_text="*",
                             required=False)


class AddProductForm(forms.Form):
    shop = forms.ModelChoiceField(
        label="Wybierz salon/magazyn dla nowego produktu",
        queryset=Sklep.objects.filter(serwis_zew=False),
        required=False)
    prf = forms.ModelChoiceField(label="Wybierz kategorię główną",
                                 queryset=Profile.objects.all(),
                                 required=True)
    ctg = forms.ModelChoiceField(label="Wybierz kategorię",
                                 queryset=Categorys.objects.all(),
                                 required=True)
    factory_id = forms.ModelChoiceField(label="Wybierz fabryke *",
                                        queryset=Factory.objects.all(),
                                        required=False)
    mark_id = forms.ModelChoiceField(label="Wybierz markę produktu *",
                                     queryset=Marka.objects.all(),
                                     required=False)
    material_id = forms.ModelChoiceField(label="Wybierz materiał produktu *",
                                         queryset=Material.objects.all(),
                                         required=False)

    name = forms.CharField(
        label="Nazwa produktu",
        required=True,
        max_length=64,
    )
    price = forms.IntegerField(
        label="Cena produktu",
        min_value=0,
        max_value=10000,
        required=True,
    )
    price_promo = forms.IntegerField(
        label="Cena promocyjna - Opcjonalnie",
        min_value=0,
        max_value=10000,
        required=False,
    )
    sale = forms.ChoiceField(choices=SALE_SORTED,
                             label="Rodzaj wyprzedaży",
                             initial='0',
                             widget=forms.Select(),
                             required=True,
                             help_text='*')

    qty = forms.IntegerField(label="Ilość - opcja *",
                             required=False,
                             min_value=0,
                             max_value=10000,
                             help_text='*')
    info = forms.CharField(
        label="Informacja o produkcie - opcja *",
        required=False,
        widget=forms.Textarea(),
    )
    image = forms.FileField(required=True, label="Ustaw foto mini")
    alt = forms.CharField(
        label="Alternatywny tekst dla foto głównego",
        required=True,
        max_length=64,
    )
    title = forms.CharField(
        label="Tytuł-tekst-dla-foto-głównego",
        required=True,
        max_length=64,
    )


class AddMainFotoProductForm(forms.Form):
    image = forms.FileField(required=False, label="Ustaw foto mini")
    alt = forms.CharField(
        label="Alternatywny tekst dla foto głównego",
        required=True,
        max_length=64,
    )
    title = forms.CharField(
        label="Tytuł-tekst-dla-foto-głównego",
        required=True,
        max_length=64,
    )


class FilterProductForm(forms.Form):
    shops = forms.ModelChoiceField(
        label="Wybierz salon/magazyn",
        queryset=Sklep.objects.filter(serwis_zew=False),
        required=False)

    profile = forms.ModelChoiceField(label="Wybierz profil",
                                     queryset=Profile.objects.all(),
                                     required=False)
    category = forms.ModelChoiceField(label="Wybierz kategorię/typ",
                                      queryset=Categorys.objects.all(),
                                      required=False)
    factory = forms.ModelChoiceField(label="Wybierz fabrykę",
                                     queryset=Factory.objects.all(),
                                     required=False)
    mark = forms.ModelChoiceField(label="Wybierz marke/producent",
                                  queryset=Marka.objects.all(),
                                  required=False)
