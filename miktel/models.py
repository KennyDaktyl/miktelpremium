from django.db import models
from django.contrib.auth.models import AbstractUser
from miktel.choices_field import *
from django.db.models import Count

# from miktel2.function import numer_umowy
from datetime import datetime
from django.db.models import Count

from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
# miesiac = datetime.now().month
# rok = datetime.now().year


def polish_slug(string):
    string = string
    slug_string = string.replace(" ", "-")
    slug_string = slug_string.replace("ś", "s")
    slug_string = slug_string.replace("Ś", "s")
    slug_string = slug_string.replace("Ż", "z")
    slug_string = slug_string.replace("Ź", "z")
    slug_string = slug_string.replace("ż", "z")
    slug_string = slug_string.replace("ź", "z")
    slug_string = slug_string.replace("Ć", "c")
    slug_string = slug_string.replace("ć", "c")
    slug_string = slug_string.replace("Rz", "rz")
    slug_string = slug_string.replace("ą", "a")
    slug_string = slug_string.replace("ę", "e")
    slug_string = slug_string.replace("ó", "o")
    return slug_string


class MyUser(AbstractUser):
    status_osoby = models.IntegerField(verbose_name="Status w Firmie",
                                       choices=Status_User,
                                       null=True,
                                       blank=True)
    umowa = models.IntegerField(verbose_name="Rodzaj zatrudnienia",
                                choices=Rodzaj_Umowy,
                                null=True,
                                blank=True)
    foto = models.ForeignKey("Foto",
                             null=True,
                             blank=True,
                             on_delete=models.CASCADE)
    info = models.TextField(verbose_name="Info", null=True, blank=True)
    sklep = models.ManyToManyField("Sklep", related_name="Miejsce_pracy")
    sklep_dzisiaj = models.ForeignKey("Sklep",
                                      null=True,
                                      blank=True,
                                      on_delete=models.CASCADE)
    adres = models.ForeignKey("Adres",
                              null=True,
                              blank=True,
                              on_delete=models.CASCADE)
    hour_rate = models.DecimalField(max_digits=5,
                                    decimal_places=2,
                                    null=True,
                                    blank=True)

    class Meta:
        ordering = ("username", )
        verbose_name_plural = "Osoby w firmie"

    def licznik(self, uslugi):
        count = (uslugi.filter(
            pracownik=self).values("usluga").order_by("usluga").annotate(
                total=Count("usluga")))
        d = {}
        for c in count:
            d[c["usluga"]] = c["total"]
        self.wykonane_uslugi = d


class Adres(models.Model):
    ulica = models.CharField(verbose_name="Ulica", max_length=32)
    miasto = models.CharField(verbose_name="Miasto", max_length=32)
    ulica_slug = models.CharField(verbose_name="Ulica do URL",
                                  max_length=32,
                                  blank=True,
                                  null=True)
    miasto_slug = models.CharField(verbose_name="Miasto do URL",
                                   max_length=32,
                                   blank=True,
                                   null=True)
    kod = models.CharField(verbose_name="Kod pocztowy", max_length=10)
    numerTelefonu = models.CharField(verbose_name="Numer telefonu",
                                     max_length=10)

    class Meta:
        ordering = ("-id", )
        verbose_name_plural = "Adresy"

    def __str__(self):
        return str(self.ulica) + ", " + str(self.miasto)


class Foto(models.Model):
    foto = models.ImageField(upload_to="images/")
    title = models.CharField(max_length=128, blank=True, null=True)
    alt = models.CharField(max_length=128, blank=True, null=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.foto)


class Sklep(models.Model):
    nazwa = models.CharField(verbose_name="Nazwa", max_length=64)
    nazwa_slug = models.CharField(verbose_name="Nazwa do URL",
                                  max_length=64,
                                  blank=True,
                                  null=True)
    foto = models.ImageField(verbose_name="Foto",
                             upload_to="images/",
                             null=True,
                             blank=True)
    adres = models.ForeignKey("Adres", on_delete=models.CASCADE)
    serwis_zew = models.BooleanField(default=False)

    class Meta:
        ordering = ("nazwa", )
        verbose_name_plural = "Nasze sklepy"

    def telefony_mag(self):
        telefony = Telefon.objects.filter(dostepny=True).filter(
            zawieszony=False).filter(magazyn_aktualny=self).count()
        telefony_mag = telefony
        return telefony_mag

    def phones_price_sum(self):
        phones_price_sum = 0
        phones = Telefon.objects.filter(magazyn_aktualny=self).filter(
            dostepny=True).filter(zawieszony=False)
        for el in phones:
            phones_price_sum += el.cena_zak
        return round(phones_price_sum, 2)

    def telefony_mag_zaw(self):
        telefony = Telefon.objects.filter(dostepny=True).filter(
            zawieszony=True).filter(magazyn_aktualny=self).count()
        telefony_mag_zaw = telefony
        return telefony_mag_zaw

    def telefony_buy(self):
        telefony = PremiaJob.objects.filter(usluga__zakup=True).filter(
            sklep=self).filter(data__month=datetime.now().month,
                               data__year=datetime.now().year).count()
        telefony_buy = telefony
        return telefony_buy

    def telefony_sell(self):
        telefony = PremiaJob.objects.filter(usluga__sprzedaz=True).filter(
            sklep=self).filter(data__month=datetime.now().month,
                               data__year=datetime.now().year).count()
        telefony_sell = telefony
        return telefony_sell

    def czesci_mag(self):
        czesci = Czesc.objects.filter(dostepny=True).filter(sklep=self)
        # czesci_mag = czesci
        tab = []
        for el in czesci:
            tab.append(el.ilosc)
        suma = sum(tab)
        return suma

    def serwis_mag(self):

        serwis = DodajSerwis.objects.filter(status=1).filter(
            sklep=self).filter(data__month=datetime.now().month,
                               data__year=datetime.now().year).count()
        serwis_mag = serwis
        return serwis_mag

    def serwis_ready(self):
        serwis = DodajSerwis.objects.filter(status=4).filter(
            sklep=self).filter(data_wydania__month=datetime.now().month,
                               data_wydania__year=datetime.now().year).count()
        serwis_ready = serwis
        return serwis_ready

    def serwis_month(self):

        serwis = DodajSerwis.objects.filter(status=5).filter(
            sklep=self).filter(data_wydania__month=datetime.now().month,
                               data_wydania__year=datetime.now().year).count()
        serwis_month = serwis
        return serwis_month

    def serwis_reklamacja(self):

        serwis_reklamacja = DodajSerwis.objects.filter(status=7).filter(
            sklep=self).filter(data__month=datetime.now().month,
                               data__year=datetime.now().year).count()
        reklamacja_seriws = serwis_reklamacja
        return reklamacja_seriws

    def serwis_zysk(self):

        serwis_zysk = PremiaJob.objects.filter(usluga__czesci=True).filter(
            sklep=self).filter(data__month=datetime.now().month,
                               data__year=datetime.now().year)
        zysk = []
        if len(serwis_zysk) > 0:
            for el in serwis_zysk:
                zysk.append(el.cena_klient - el.koszt)
                zysk_gsm = sum(zysk)
        else:
            zysk = [0]
            zysk_gsm = sum(zysk)
        return zysk_gsm

    def serwis_g_zysk(self):

        serwis_zysk = PremiaJob.objects.filter(usluga__grawer=True).filter(
            sklep=self).filter(data__month=datetime.now().month,
                               data__year=datetime.now().year)
        zysk = []
        if len(serwis_zysk) > 0:
            for el in serwis_zysk:
                zysk.append(el.cena_klient - el.koszt)
                zysk_gsm = sum(zysk)
        else:
            zysk = [0]
            zysk_gsm = sum(zysk)
        return zysk_gsm

        el.serwis_g_zysk

    def __str__(self):
        return str(self.nazwa) + ", " + str(self.adres.ulica)


# Dokumenty i telefony
class UmowaKomisowaNew(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(verbose_name="Numer umowa",
                              max_length=64,
                              null=True,
                              blank=True)
    sklep_zak = models.ForeignKey("Sklep",
                                  on_delete=models.CASCADE,
                                  verbose_name="Miejsce zakupu",
                                  default=1)
    komitent = models.CharField(verbose_name="Dane komitenta", max_length=128)
    adres_komitenta = models.CharField(verbose_name="Adres komitenta",
                                       max_length=128)
    numer_dowodu = models.CharField(verbose_name="Numer dowodu", max_length=9)
    data_zak = models.DateTimeField(auto_now_add=True)
    sprzedana = models.BooleanField(default=False)
    data_sprzed = models.DateTimeField(null=True, blank=True)
    pracownik_zak = models.ForeignKey(
        "MyUser",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="pracownik_kupujący",
    )
    pracownik_sprzed = models.ForeignKey(
        "MyUser",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="pracownik_sprzedaż",
    )
    phones = models.ForeignKey("Telefon",
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)

    class Meta:
        ordering = ("-id", )
        verbose_name_plural = "Umowy komisowe"

    def __str__(self):
        return str(self.number) + ", " + str(self.id)


class Telefon(models.Model):
    marka = models.ForeignKey(
        "Marka",
        on_delete=models.CASCADE,
    )
    stan = models.IntegerField(verbose_name="Stan telefon",
                               choices=StanTelefonu)
    kategoria = models.ForeignKey("Kategoria", on_delete=models.CASCADE)
    nazwa = models.CharField(verbose_name="Model", max_length=64)
    imei = models.CharField(verbose_name="imei", max_length=15)
    cena_zak = models.FloatField()
    cena_sprzed = models.FloatField(blank=True, null=True)
    sklep = models.ForeignKey("Sklep",
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True)
    sklep_sprzed = models.ForeignKey("Sklep",
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True,
                                     related_name="sklep_sprzadzy")

    dostepny = models.BooleanField(default=True)
    zawieszony = models.BooleanField(default=False)
    dokument = models.BooleanField(default=False)

    pracownik_zak = models.ForeignKey(
        "MyUser",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="przyjmowal",
    )
    pracownik_sprzed = models.ForeignKey(
        "MyUser",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="sprzdawal",
    )
    data_wprow = models.DateField(
        null=True,
        blank=True,
    )
    data_sprzed = models.DateField(
        null=True,
        blank=True,
    )
    data_zmiany = models.DateField(
        verbose_name="Data zmiany (YYYY-MM-DD)",
        null=True,
        blank=True,
    )
    nr_doc = models.CharField(
        verbose_name="Nr dokumentu",
        max_length=64,
        blank=True,
        null=True,
    )
    magazyn_aktualny = models.ForeignKey("Sklep",
                                         verbose_name="Aktualnie dostępny w:",
                                         on_delete=models.CASCADE,
                                         blank=True,
                                         null=True,
                                         related_name="Sklep_aktualny")
    info = models.CharField(
        verbose_name="Informacje",
        max_length=256,
        blank=True,
        null=True,
    )

    foto = models.ManyToManyField("Foto", blank=True)

    class Meta:
        ordering = ("-id", "marka", "nazwa", "kategoria")
        verbose_name_plural = "Telefony"

    @property
    def zysk(self):
        zysk = self.cena_sprzed - self.cena_zak
        return zysk

    @property
    def total_price(self):
        total = []
        faktura = FakturaZakupu.objects.all()
        for el in faktura:
            total.append(el.cena_zak)
        total_price = sum[total]

        return total_price

    @property
    def search_document(self, pk):
        fv = self.objects.filter(pk=pk)
        for el in fv:
            for tele in el.telefon.all():
                if tele.id == self.id:

                    return (el.numer)

    @property
    def price_minus_vat(self):
        price_tax = round(self.cena_zak / 1.23, 2)
        return price_tax

    def foto_mini(self):
        foto_mini = FotoProduct.objects.filter(phone_id=self.id).filter(
            mini=True).first()

        if foto_mini is None:
            foto_mini = FotoProduct.objects.filter(mark_id=self.marka).filter(
                default=True).first()
            if foto_mini is None:
                foto_mini = FotoProduct.objects.filter(nofoto=True).first()
        return foto_mini

    def __str__(self):
        return str(self.id) + " " + str(self.marka) + " " + str(
            self.nazwa) + " " + str(self.imei)

    slug = models.SlugField(verbose_name="Nazwa slug",
                            blank=True,
                            null=True,
                            max_length=256)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nazwa) + "-" + slugify(
            self.marka.nazwa) + "-" + slugify(
                self.kategoria.nazwa) + "-" + slugify(
                    STAN[self.stan][1]) + "-dostepny-w-" + slugify(
                        self.magazyn_aktualny)
        super(Telefon, self).save()

    def get_absolute_url(self):
        return reverse("store_gsm_phones_details_view",
                       kwargs={
                           "slug": self.slug,
                           "id": self.id,
                       })


class Marka(models.Model):
    nazwa = models.CharField(max_length=64)

    class Meta:
        ordering = ("nazwa", )
        verbose_name_plural = "Marki telefonów"

    def __str__(self):
        return str(self.nazwa)


class Kategoria(models.Model):
    nazwa = models.CharField(max_length=64)

    class Meta:
        ordering = ("nazwa", )
        verbose_name_plural = "Kategorie telefonów GSM"

    def __str__(self):
        return str(self.nazwa)


class FakturaZakupu(models.Model):
    numer = models.CharField(max_length=64)
    data_zak = models.DateField(auto_now_add=True)
    hurtownia = models.ForeignKey("Hurtownia", on_delete=models.CASCADE)
    sklep = models.ForeignKey("Sklep", on_delete=models.CASCADE, default=1)
    telefon = models.ManyToManyField("Telefon")
    pracownik_zak = models.ForeignKey("MyUser", on_delete=models.CASCADE)

    def invoice_sum(self):
        suma = 0
        for phone in self.telefon.all():
            suma += phone.cena_zak
        suma = round(suma, 2)
        return suma

    class Meta:
        ordering = ("-id", )
        verbose_name_plural = "Faktury"

    def __str__(self):
        return str(self.numer) + " " + str(self.hurtownia.nazwa)


class Hurtownia(models.Model):
    nazwa = models.CharField(max_length=64)

    class Meta:
        ordering = ("nazwa", )
        verbose_name_plural = "Nasi dostawcy"

    def __str__(self):
        return str(self.nazwa)


class Usluga(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=64)
    sklep = models.ManyToManyField("Sklep")
    typ = models.IntegerField(verbose_name="Typ prowizji",
                              choices=RODZAJ_PROWIZJI,
                              default=0)
    kwota = models.IntegerField(default=0)
    czesci = models.BooleanField(default=False)
    zakup = models.BooleanField(default=False)
    sprzedaz = models.BooleanField(default=False)
    grawer = models.BooleanField(default=False)
    akcesoria = models.BooleanField(default=False)

    # akcesoria = models.BooleanField(default=False)

    class Meta:
        ordering = ("nazwa", )
        verbose_name_plural = "Usługi nazwa"

    def __str__(self):
        return str(self.nazwa)


class PremiaJob(models.Model):
    check = models.IntegerField(default=0)
    sklep = models.ForeignKey("Sklep", on_delete=models.CASCADE)
    pracownik = models.ForeignKey("MyUser", on_delete=models.CASCADE)
    usluga = models.ForeignKey("Usluga", on_delete=models.CASCADE)
    model = models.CharField(max_length=128, blank=True, null=True)
    cena_klient = models.IntegerField(verbose_name="Cena klient",
                                      blank=True,
                                      null=True,
                                      default=0)
    koszt = models.IntegerField(verbose_name="Koszty",
                                blank=True,
                                null=True,
                                default=0)
    data = models.DateTimeField(auto_now_add=True)

    @property
    def get_zysk(self):
        if self.cena_klient > self.koszt:
            zysk = self.cena_klient - self.koszt
            return zysk
        else:
            zysk = 0
            return zysk

    @property
    def show_premia(self):
        if self.cena_klient != "" and self.koszt != "" and self.cena_klient >= self.koszt:
            if self.usluga.typ == 0:
                return (self.cena_klient - self.koszt) * (
                    (self.usluga.kwota)) / 100
            else:
                return self.usluga.kwota
        else:
            c = "Brak premii"
            return c

    def get_services(self, serwisant):
        services = self.objects.filter(serwisant=serwisant)
        d = {}
        for service in services:
            if d.get(service.usluga):
                d[service.usluga.id] += 1
            else:
                d[service.usluga.id] = 1
        return d

    @property
    def counter(self):
        counter = self.serwisant.id
        return counter

    @property
    def pokaz_sumeGSM_1(self):
        uslugi = Usluga.objects.all()
        pracownicy = MyUser.objects.all()
        serwisy = MyUser.objects.all()
        diction = {}
        for usluga in uslugi:
            for serwis in serwisy:
                counter = (MyUser.objects.filter(
                    serwisant=self.serwisant).filter(
                        usluga=self.usluga).count())
                diction[usluga.id] = counter
            return diction

    class Meta:
        ordering = ("id", )
        verbose_name_plural = "Premie pracowników"

    def __str__(self):
        return str(self.check) + " " + str(self.data) + " " + str(
            self.usluga.nazwa) + " " + str(self.usluga) + " " + str(
                self.pracownik)


class InnePracePremiowane(models.Model):
    nazwa = models.CharField(verbose_name="Nazwa czynności premiowanej",
                             max_length=128)
    pracownik = models.ForeignKey('MyUser', on_delete=models.CASCADE)
    czas = models.IntegerField(
        verbose_name="Czas trwania w godzinach lub ilość")
    opis = models.TextField(verbose_name="Opis wykonanje czynności",
                            blank=True,
                            null=True)
    data = models.DateField(auto_now_add=True, verbose_name="Data")

    class Meta:
        ordering = (
            "nazwa",
            "pracownik",
        )
        verbose_name_plural = "Inne prace"

    def __str__(self):
        return str(self.nazwa) + " " + str(self.czas) + "h"


class DodajSerwis(models.Model):
    sklep = models.ForeignKey("Sklep", on_delete=models.CASCADE)

    pracownik = models.ForeignKey("MyUser",
                                  on_delete=models.CASCADE,
                                  related_name="Przyjmujacy")
    serwisant = models.ForeignKey(
        "MyUser",
        on_delete=models.CASCADE,
        related_name="Naprawiajacy",
        blank=True,
        null=True,
    )
    usluga = models.ForeignKey("Usluga", on_delete=models.CASCADE)
    marka = models.ForeignKey("Marka",
                              verbose_name="Wybierz marke",
                              on_delete=models.CASCADE,
                              default=1)
    model = models.CharField(max_length=128, blank=True, null=True)
    imei = models.CharField(max_length=15, blank=True, null=True)
    cena_zgoda = models.IntegerField(verbose_name="Cena naprawy",
                                     blank=True,
                                     null=True,
                                     default=0)
    koszt = models.IntegerField(verbose_name="Koszty",
                                blank=True,
                                null=True,
                                default=0)
    data = models.DateTimeField(auto_now_add=True)
    data_wydania = models.DateTimeField(blank=True, null=True)
    numer_telefonu = models.CharField(max_length=9, blank=True, null=True)
    imie_nazwisko = models.CharField(max_length=64, blank=True, null=True)
    status = models.IntegerField(verbose_name="Status naprawy",
                                 choices=STATUS_NAPRAWY,
                                 default=1)
    info = models.CharField(max_length=256, blank=True, null=True)
    archiwum = models.BooleanField(default=False)
    naprawa = models.BooleanField(default=True)

    def get_service_zysk(self):
        zysk = self.cena_zgoda - self.koszt
        zysk = round(zysk, 2)
        return zysk

    class Meta:
        ordering = (
            "data",
            "marka",
            "model",
        )
        verbose_name_plural = "Serwisy gsm"

    def __str__(self):
        return str(self.id) + " " + str(self.data) + " " + str(
            self.marka) + " " + str(self.model) + " " + str(self.usluga)


class Czesc(models.Model):
    id = models.AutoField(primary_key=True)

    foto = models.ManyToManyField("Foto",
                                  verbose_name="Foto_produktu",
                                  blank=True)
    marka = models.ForeignKey("Marka", on_delete=models.CASCADE)
    typ = models.ForeignKey("Typ", on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=64)
    stan = models.IntegerField(verbose_name="Stan czesci",
                               choices=StanCzesci,
                               default=0)
    kolor = models.IntegerField(verbose_name="Kolor czesci",
                                choices=Kolor,
                                default=0)
    date_add = models.DateField(auto_now_add=True)
    cena_zak = models.IntegerField()
    cena_sprzed = models.IntegerField(blank=True, null=True)
    ilosc = models.IntegerField()
    opis = models.CharField(max_length=128, blank=True, null=True)
    sklep = models.ForeignKey("Sklep",
                              verbose_name="Magazyn",
                              on_delete=models.CASCADE)
    pracownik = models.ForeignKey("MyUser",
                                  verbose_name="Wprowadził",
                                  on_delete=models.CASCADE,
                                  default=1)
    dostepny = models.BooleanField(default=True)

    # @property
    def name_slug(self):
        slug_name = self.nazwa.replace(" ", "-")
        slug_name = slug_name.replace("ś", "s")
        # slug_name = encodePL(slug_name)
        return slug_name

    def typ_slug(self):
        slug_typ = self.typ.nazwa.replace(" ", "-")
        slug_typ = slug_typ.replace("ś", "s")
        # slug_typ = encodePL(slug_typ)
        return slug_typ

    def foto_mini(self):
        foto_mini = FotoProduct.objects.filter(phone_id=self.id).filter(
            mini=True).first()

        if foto_mini is None:
            foto_mini = FotoProduct.objects.filter(mark_id=self.marka).filter(
                default=True).first()
            if foto_mini is None:
                foto_mini = FotoProduct.objects.filter(nofoto=True).first()
        return foto_mini

    def search_def(self):
        return self.marka.nazwa + ", " + self.nazwa + ", " + self.typ.nazwa

    class Meta:
        ordering = (
            "marka",
            "nazwa",
            "typ",
        )
        verbose_name_plural = "Czesci_gsm"

    def __str__(self):
        return str(self.id) + " " + str(self.nazwa) + " " + str(
            self.typ) + " " + str(self.marka) + " " + str(
                self.kolor) + " " + str(self.cena_sprzed) + " " + str(
                    self.sklep)

    slug = models.SlugField(verbose_name="Nazwa slug",
                            blank=True,
                            null=True,
                            max_length=256)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nazwa) + "-" + slugify(
            self.marka.nazwa) + "-" + slugify(self.typ.nazwa) + "-" + slugify(
                Kolor[self.kolor][1]) + "-dostepny-w-" + slugify(self.sklep)
        # self.slug.save()
        super(Czesc, self).save()

    def get_absolute_url(self):
        return reverse("store_gsm_item_details_view",
                       kwargs={
                           "slug": self.slug,
                           "id": self.id,
                       })


class Typ(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=64)

    class Meta:
        ordering = ("nazwa", )
        verbose_name_plural = "Typ czesci"

    def typ_slug(self):
        slug = polish_slug(str(self.nazwa))
        return slug

    def __str__(self):
        return str(self.nazwa)


class Material(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        ordering = ("name", )
        verbose_name_plural = "Materiał"

    def typ_slug(self):
        slug = polish_slug(str(self.name))
        return slug

    def __str__(self):
        return str(self.name)


class Products(models.Model):
    date = models.DateField(auto_now_add=True)
    user_id = models.ForeignKey("MyUSer",
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)
    mark_id = models.ForeignKey("Marka",
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)
    name = models.CharField(max_length=64)
    category_id = models.ForeignKey("Categorys",
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True)
    shop_id = models.ForeignKey("Sklep",
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)
    factory_id = models.ForeignKey("Factory",
                                   on_delete=models.CASCADE,
                                   blank=True,
                                   null=True)
    material_id = models.ForeignKey("Material",
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True)
    qty = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    price_promo = models.FloatField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_new = models.BooleanField(default=False)
    is_promo = models.BooleanField(default=False)

    info = models.TextField(blank=True, null=True)

    def foto_mini(self):
        foto_mini = FotoProduct.objects.filter(product_id=self.id).filter(
            main=True).first()
        return foto_mini

    def foto_lightbox(self):
        fotos = FotoProduct.objects.filter(product_id=self.id).order_by('id')
        fotos_mix = {}
        i = 0
        for i in range(len(fotos)):
            if fotos[i].another_min == True:
                fotos_mix.update({fotos[i]: fotos[i - 1]})
        return fotos_mix

    class Meta:
        ordering = ("name", )
        verbose_name_plural = "Produkty w sklepie"

    def __str__(self):
        return str(self.id) + ", " + str(self.name)

    slug = models.SlugField(verbose_name="Nazwa slug",
                            blank=True,
                            null=True,
                            max_length=128)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        # self.slug.save()
        super(Products, self).save()

    def get_absolute_url(self):
        return reverse("products",
                       kwargs={
                           "cat": self.category_id.profile_id.slug,
                           "slug": self.category_id.slug,
                           "name": self.slug,
                           "id": self.id
                       })


class Factory(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    name_slug = models.CharField(max_length=64, blank=True, null=True)
    accessories = models.BooleanField(default=False)

    def foto_mini(self):
        foto_mini = FotoProduct.objects.filter(category_id=self.id).filter(
            main=True).first()
        return foto_mini

    class Meta:
        ordering = ("name", )
        verbose_name_plural = "Producent"

    def __str__(self):
        return str(self.name)


class Categorys(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    name_slug = models.CharField(max_length=64, blank=True, null=True)
    profile_id = models.ForeignKey("Profile",
                                   on_delete=models.CASCADE,
                                   blank=True,
                                   null=True)

    accessories = models.BooleanField(default=False)

    def foto_mini(self):
        foto_mini = FotoProduct.objects.filter(category_id=self.id).filter(
            main=True).first()

        # if foto_mini is None:
        #     foto_mini = FotoProduct.objects.filter(mark_id=self.marka).filter(
        #         default=True).first()
        #     if foto_mini is None:
        #         foto_mini = FotoProduct.objects.filter(nofoto=True).first()
        return foto_mini

    class Meta:
        ordering = ("name", )
        verbose_name_plural = "Kategorie"

    slug = models.SlugField(verbose_name="Nazwa slug",
                            blank=True,
                            null=True,
                            max_length=256)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Categorys, self).save()

    def get_absolute_url(self):
        return reverse("categorys",
                       kwargs={
                           "cat": self.profile_id.slug,
                           "slug": self.slug,
                       })

    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def foto_mini(self):
        foto_mini = FotoProduct.objects.filter(category_id=self.id).filter(
            main=True).first()
        return foto_mini

    class Meta:
        ordering = ("name", )
        verbose_name_plural = "Kategorie główne"

    slug = models.SlugField(verbose_name="Nazwa slug",
                            blank=True,
                            null=True,
                            max_length=256)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Profile, self).save()

    def __str__(self):
        return str(self.name)


class ProductDetails(models.Model):
    phone_id = models.OneToOneField("Telefon",
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True)
    product_id = models.OneToOneField("Products",
                                      on_delete=models.CASCADE,
                                      blank=True,
                                      null=True)
    item_id = models.OneToOneField("Czesc",
                                   on_delete=models.CASCADE,
                                   blank=True,
                                   null=True)
    aparat_a = models.CharField(max_length=32)
    aparat_b = models.CharField(max_length=32)
    battery = models.CharField(max_length=32)
    system = models.CharField(max_length=32)
    info = models.CharField(max_length=64)

    class Meta:
        ordering = ("phone_id", )
        verbose_name_plural = "Szczegóły produktu"

    def __str__(self):
        return str(self.aparat_a) + ", " + str(self.aparat_b) + ", " + str(
            self.battery) + ", " + str(self.system) + ", " + str(self.info)


class FotoProduct(models.Model):
    image = models.ImageField(upload_to="images/")
    product_details = models.ForeignKey("ProductDetails",
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        null=True)
    phone_id = models.ForeignKey("Telefon",
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True)
    item_id = models.ForeignKey("Czesc",
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)
    product_id = models.ForeignKey("Products",
                                   on_delete=models.CASCADE,
                                   blank=True,
                                   null=True)
    category_id = models.ForeignKey("Categorys",
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True)
    mark_id = models.ForeignKey("Marka",
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)
    title = models.CharField(max_length=64, blank=True, null=True)
    alt = models.CharField(max_length=64, blank=True, null=True)
    used = models.BooleanField(default=False)
    mini = models.BooleanField(default=False)
    main = models.BooleanField(default=False)
    another = models.BooleanField(default=False)
    another_min = models.BooleanField(default=False)
    default = models.BooleanField(default=False)
    nofoto = models.BooleanField(default=False)

    class Meta:
        ordering = ("-id", )
        verbose_name_plural = "Zdjęcia produktów"

    def __str__(self):
        return str(self.image) + ", " + str(self.mini) + ", " + str(
            self.another) + ", " + str(self.another_min)


class Payment(models.Model):
    date = models.DateField(auto_now_add=True)
    user_id = models.ForeignKey("MyUser",
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)
    hours_count = models.IntegerField(blank=True, null=True)
    payment = models.IntegerField()
    is_payment = models.BooleanField(default=False)
    is_adv_payment = models.BooleanField(default=False)
    is_bonus = models.BooleanField(default=False)
    info = models.CharField(max_length=64,
                            verbose_name="Info",
                            null=True,
                            blank=True)

    class Meta:
        ordering = ("date", )
        verbose_name_plural = "Wypłaty i inne"

    def payment_real(self):
        if self.user_id.hour_rate is not None or self.user_id.hour_rate != 0:
            return self.hours_count * self.user_id.hour_rate

    def payment_difr(self):
        if self.user_id.hour_rate is not None or self.user_id.hour_rate != 0:
            return self.payment - (self.hours_count * self.user_id.hour_rate)

    def __str__(self):
        return str(self.date) + ", " + str(self.user_id) + ", " +\
                str(self.hours_count)


class WorkSchedule(models.Model):
    date = models.DateField()
    time_start = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)
    user_id = models.ForeignKey("MyUser",
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)
    shop = models.ForeignKey("Sklep",
                             verbose_name="Magazyn",
                             on_delete=models.CASCADE)

    # hours = models.IntegerField(blank=True, null=True)
    time_duration = models.TimeField(blank=True, null=True)

    def hours_count_def(self):
        from datetime import datetime, timedelta
        if self.time_start and self.time_end != None:
            time_start_h = str(self.time_start)[0:2]
            time_start_m = str(self.time_start)[3:5]
            time_end_h = str(self.time_end)[0:2]
            time_end_m = str(self.time_end)[3:5]
            hours = timedelta(
                hours=int(time_end_h), minutes=int(time_end_m)) - timedelta(
                    hours=int(time_start_h), minutes=int(time_start_m))
            return hours
        else:
            return None

    class Meta:
        ordering = ("-date", "-time_duration")
        verbose_name_plural = "Grafik"

    def __str__(self):
        return str(self.date) + ", " + str(self.user_id) + ", " +\
                str(self.shop)+ ", " +\
                str(self.time_start)+ ", " +\
                str(self.time_end)
