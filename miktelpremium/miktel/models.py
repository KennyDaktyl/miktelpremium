from django.db import models
from django.contrib.auth.models import AbstractUser
from miktel.choices_field import *
from django.db.models import Count

# from miktel2.function import numer_umowy
from datetime import datetime
from django.db.models import Count

# Create your models here.
miesiac = datetime.now().month
rok = datetime.now().year


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

    def licznik(self, uslugi):
        count = (uslugi.filter(
            pracownik=self).values("usluga").order_by("usluga").annotate(
                total=Count("usluga")))
        d = {}
        for c in count:
            d[c["usluga"]] = c["total"]
        self.wykonane_uslugi = d


class Adres(models.Model):
    ulica = models.CharField(verbose_name="Ulica", max_length=128)
    miasto = models.CharField(verbose_name="Miasto", max_length=128)
    kod = models.CharField(verbose_name="Kod pocztowy", max_length=128)
    numerTelefonu = models.CharField(verbose_name="Numer telefonu",
                                     max_length=128)

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
    foto = models.ImageField(verbose_name="Foto",
                             upload_to="images/",
                             null=True,
                             blank=True)
    adres = models.ForeignKey("Adres", on_delete=models.CASCADE)
    serwis_zew = models.BooleanField(default=False)

    class Meta:
        ordering = ("nazwa", )

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
            sklep=self).filter(data__month=miesiac, data__year=rok).count()
        telefony_buy = telefony
        return telefony_buy

    def telefony_sell(self):
        telefony = PremiaJob.objects.filter(usluga__sprzedaz=True).filter(
            sklep=self).filter(data__month=miesiac, data__year=rok).count()
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
            sklep=self).filter(data__month=miesiac, data__year=rok).count()
        serwis_mag = serwis
        return serwis_mag

    def serwis_ready(self):
        serwis = DodajSerwis.objects.filter(status=4).filter(
            sklep=self).filter(data_wydania__month=miesiac,
                               data_wydania__year=rok).count()
        serwis_ready = serwis
        return serwis_ready

    def serwis_month(self):

        serwis = DodajSerwis.objects.filter(status=5).filter(
            sklep=self).filter(data_wydania__month=miesiac,
                               data_wydania__year=rok).count()
        serwis_month = serwis
        return serwis_month

    def serwis_reklamacja(self):

        serwis_reklamacja = DodajSerwis.objects.filter(status=7).filter(
            sklep=self).filter(data__month=miesiac, data__year=rok).count()
        reklamacja_seriws = serwis_reklamacja
        return reklamacja_seriws

    def serwis_zysk(self):

        serwis_zysk = PremiaJob.objects.filter(usluga__czesci=True).filter(
            sklep=self).filter(data__month=miesiac, data__year=rok)
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
            sklep=self).filter(data__month=miesiac, data__year=rok)
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
        return str(self.nazwa) + ", " + str(self.adres.miasto)


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

    # def get_free_phone(self, telefon_id):
    #     phone_free = self.objects.filter(dokument=False)

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

    # zdjecia = models.ManyToManyField("Foto", blank=True)

    class Meta:
        ordering = ("-id", "marka", "nazwa")

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

    def __str__(self):
        return str(self.id) + " " + str(self.marka) + " " + str(
            self.nazwa) + " " + str(self.imei)
        # return str(self.nazwa) + " " + str(self.imei)


class Marka(models.Model):
    nazwa = models.CharField(max_length=64)

    class Meta:
        ordering = ("nazwa", )

    def __str__(self):
        return str(self.nazwa)


class Kategoria(models.Model):
    nazwa = models.CharField(max_length=64)

    class Meta:
        ordering = ("nazwa", )

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

    def __str__(self):
        return str(self.numer) + " " + str(self.hurtownia.nazwa)


class Hurtownia(models.Model):
    nazwa = models.CharField(max_length=64)

    class Meta:
        ordering = ("nazwa", )

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

    def __str__(self):
        return str(self.check) + " " + str(self.data) + " " + str(self.usluga.nazwa) + " " + str(
            self.usluga) + " " + str(self.pracownik)


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

    class Meta:
        ordering = (
            "marka",
            "typ",
            "nazwa",
        )

    def __str__(self):
        return str(self.nazwa) + " " + str(self.typ)


class Typ(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=64)

    class Meta:
        ordering = ("nazwa", )

    def __str__(self):
        return str(self.nazwa)
