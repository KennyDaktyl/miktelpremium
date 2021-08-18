from django.contrib import admin

# Pobieram UserAdmin i dziedzicze go dla rejestracji mojego modelu MyUser-a ponieważ dzięki temu nowy użytkownik będzie miał hashowane hasło podczas tworzenia

from miktel.models import *

# Register your models here.
admin.site.register(Articles)
admin.site.register(MyUser)
admin.site.register(Profile)
admin.site.register(Factory)
admin.site.register(Foto)
admin.site.register(WorkSchedule)
admin.site.register(Payment)
admin.site.register(Products)
admin.site.register(Categorys)
admin.site.register(ProductDetails)
admin.site.register(FotoProduct)
admin.site.register(Adres)
admin.site.register(Sklep)
# admin.site.register(Telefon)
# admin.site.register(UmowaKomisowaNew)
admin.site.register(Marka)
admin.site.register(Kategoria)
# admin.site.register(FakturaZakupu)
admin.site.register(Hurtownia)
# admin.site.register(PremiaJob)
admin.site.register(Usluga)
# admin.site.register(DodajSerwis)
admin.site.register(Typ)
admin.site.register(Czesc)
admin.site.register(InnePracePremiowane)


@admin.register(DodajSerwis)
class Seriveces(admin.ModelAdmin):
    list_display = ('id', 'sklep', 'pracownik', 'serwisant', 'usluga', 'marka',
                    'model', 'imei', 'cena_zgoda', 'koszt', 'data',
                    'data_wydania', 'status', 'archiwum', 'info', 'naprawa')
    list_filter = ('sklep', 'serwisant', 'usluga', 'status')
    search_fields = ('id', 'imei', 'model')
    ordering = ('-id', )


@admin.register(PremiaJob)
class Bonus(admin.ModelAdmin):
    list_display = ('id', 'check', 'sklep', 'pracownik', 'usluga', 'model',
                    'cena_klient', 'koszt', 'data', 'show_premia')
    list_filter = ('sklep', 'pracownik')
    search_fields = ('id', 'check', 'model')
    ordering = ('-id', )


@admin.register(Telefon)
class Phones(admin.ModelAdmin):
    list_display = (
        'id',
        'sklep',
        'sklep_sprzed',
        'stan',
        'kategoria',
        'marka',
        'nazwa',
        'imei',
        'cena_zak',
        'cena_sprzed',
        'cena_promo',
        'in_promo',
        'dostepny',
        'zawieszony',
        'dokument',
    )
    list_filter = ('dostepny', 'sklep', 'sklep_sprzed', 'marka')
    search_fields = ('id', 'imei', 'nazwa')
    ordering = ('-id', )


@admin.register(FakturaZakupu)
class Invoice(admin.ModelAdmin):
    list_display = (
        'id',
        'data_zak',
        'sklep',
        'numer',
        'hurtownia',
        'pracownik_zak',
    )
    list_filter = (
        'sklep',
        'pracownik_zak',
    )
    search_fields = ('id', 'numer')
    ordering = ('-id', )


@admin.register(UmowaKomisowaNew)
class Umowy(admin.ModelAdmin):
    list_display = ('id', 'data_zak', 'sklep_zak', 'number', 'phones',
                    'komitent', 'adres_komitenta', 'numer_dowodu',
                    'pracownik_zak', 'data_sprzed', 'sprzedana',
                    'pracownik_sprzed')
    list_filter = (
        'sklep_zak',
        'pracownik_zak',
    )
    search_fields = ('id', 'number', 'phones__nazwa', 'phones__imei',
                     'komitent')
    ordering = ('-id', )