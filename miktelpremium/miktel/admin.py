from django.contrib import admin

# Pobieram UserAdmin i dziedzicze go dla rejestracji mojego modelu MyUser-a ponieważ dzięki temu nowy użytkownik będzie miał hashowane hasło podczas tworzenia
from django.contrib.auth.admin import UserAdmin

from miktel.models import *

# Register your models here.

admin.site.register(MyUser)
admin.site.register(Foto)
admin.site.register(Adres)
admin.site.register(Sklep)
admin.site.register(Telefon)
admin.site.register(UmowaKomisowaNew)
admin.site.register(Marka)
admin.site.register(Kategoria)
admin.site.register(FakturaZakupu)
admin.site.register(Hurtownia)
admin.site.register(PremiaJob)
admin.site.register(Usluga)
admin.site.register(DodajSerwis)
admin.site.register(Typ)
admin.site.register(Czesc)
