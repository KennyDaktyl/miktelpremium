from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from miktel.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path('dodaj_uzytkownika/',
         DodajMyUserView.as_view(),
         name="dodaj_uzytkownika"),
    path('lista_uzytkownikow/',
         ListaMyUserView.as_view(),
         name="lista_uzytkownikow"),
    path('edycja_uzytkownika/<int:pk>',
         EdycjaMyUserView.as_view(),
         name="edycja_uzytkownika"),
    path('telefony_magazyn/',
         TelefonyMagazynView.as_view(),
         name="telefony_magazyn"),
    path('sell_phones/<int:pk>', SellPhonesView.as_view(), name="sell_phone"),

    path('telefony_sprzedane/',
         TelefonySprzedaneView.as_view(),
         name="telefony_sprzedane"),
    path('umowa_komisowa/', UmowaKomisowaView.as_view(),
         name="umowa_komisowa"),
    path('checking_document/',
         CheckingDocumentView.as_view(),
         name="checking_document/"),
    path('umowa_imei/<int:pk>', UmowaIdView.as_view(), name="umowa_imei"),

    path('faktura_imei/<int:pk>', FakturaIdView.as_view(),
         name="faktura_imei"),
    path('faktura_zakupu/', FakturaZakupuView.as_view(),
         name="faktura_zakupu"),
    path('checking_invoice/',
         CheckingInvoiceView.as_view(),
         name="checking_invoice"),
    path('dodaj_telefon/', TelefonCreateView.as_view(), name="dodaj_telefon"),
    path('dodaj_serwis/', DodajSerwisView.as_view(), name="dodaj_serwis"),
    path('szczegoly_serwisu/<int:pk>',
         SzczegolySerwisuView.as_view(),
         name='szczegoly_serwisu'),
    path('gotowy_do_odbioru/<int:pk>',
         GotowySerwisView.as_view(),
         name='gotowy_serwis'),
    path('wykonaj_serwis_z_czesciami/<int:pk>',
         GetServiceForItems.as_view(),
         name='wykonaj_serwis_z_czesciami'),
    path('save_service/<int:pk>',
         ServiceReadyView.as_view(),
         name='save_service'),
    path('sent_service/', ServiceSentView.as_view(), name='sent_service'),
    path('wydaj_serwis/<int:pk>',
         WydajSerwisView.as_view(),
         name='wydaj_serwis'),
    path('wydaj_serwis_czesci/',
         WydajSerwisCzesciView.as_view(),
         name='wydaj_serwis_czesci'),
    path('archiwum_serwisow/',
         ArchiwumSerwisView.as_view(),
         name='archiwum_serwisow'),
    path('reklamacja_serwis/<int:pk>',
         ReklamacjaSerwisView.as_view(),
         name='reklamacja_serwis'),
    path('lista_serwisow/',
         ListaSerwisowMagazynView.as_view(),
         name="lista_serwisow"),
    path('lista_serwisow_gotowych/',
         ListaSerwisowGotowychMagazynView.as_view(),
         name="lista_serwisow_gotowych"),
    path('wystaw_telefon/<int:pk>',
         WystawTelefonView.as_view(),
         name='wystaw_telefon'),
    path('szczegoly_telefonu/<int:pk>',
         SzczegolyTelefonuView.as_view(),
         name='szczegoly_telefonu'),
    path('delete_document/<int:pk>',
         DeleteDocumentView.as_view(),
         name="delete_document"),
    path('lista_umow/', ListaUmowView.as_view(), name="lista_umow"),
    path('edycja_umowy/<int:pk>',
         EdycjaUmowyView.as_view(),
         name="edycja_umowy"),
    path('lista_faktur/', ListaFakturView.as_view(), name="lista_faktur"),
    path('edycja_faktury/<int:pk>',
         EdycjaFakturyView.as_view(),
         name="edycja_faktury"),
    path('wystaw_telefon/<int:pk>',
         WystawTelefonView.as_view(),
         name='wystaw_telefon'),
    path('generuj_pdf/<int:pk>', GenerujPdfView.as_view(), name='pdf_umowa'),
    path('lista_uslug/', ListaUslugView.as_view(), name="lista_uslug"),
    path('dodaj_usluge/', DodajUslugaView.as_view(), name="dodaj_usluge"),
    path('edycja_uslugi/<int:pk>',
         EdycjaUslugiView.as_view(),
         name="edycja_uslugi"),
    path('dashboard_sklepow/',
         DashboardView.as_view(),
         name="dashboard_sklepow"),
    path('dodaj_premiaJob/',
         DodajPremiaJobView.as_view(),
         name="dodaj_premiaJob"),
    path('twoje_premie/', TwojePremieJobView.as_view(),
         name="twoje_premieJob"),
    path('edycja_premiaJob/<int:pk>',
         EdycjaPremiaJobView.as_view(),
         name="edycja_premiaJob"),
    path('szczegoly_serwisow_serwisanta/<int:pk>/<int:miesiac>/<int:rok>/',
         SzczegolySerwisySerwisantaView.as_view(),
         name='szczegoly_serwisow_serwisanta'),
    path('dodaj_czesc/',
         CzesciCreateView.as_view(),
         name='dodaj_czesc'),
    path('lista_czesci/',
         ListaCzesciView.as_view(),
         name='lista_czesci'),
    path('szczegoly_czesci/<int:pk>',
         SzczegolyCzesciView.as_view(), name="szczegoly_czesci"),
    path('uzyj_czesci/',
         UzyjCzesciView.as_view(), name="uzyj_czesci"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('profil/<int:pk>', ProfilView.as_view(), name="profil"),
    path('logout/', User_Logout),
] + static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
