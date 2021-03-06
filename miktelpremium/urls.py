from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from miktel.views import *
from store.views import *
from store.rest_class import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import routers, serializers, viewsets, generics
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from django.views.decorators.cache import cache_page
from store.sitemaps import *
sitemaps = {
    'phone': PhoneSiteView,
    'phone_static': PhoneMainSiteView,
    'item': ItemsSiteView,
    'item_static': ItemMainSiteView,
    'categorys_gsm': CategorysGSMSiteView,
    'products': ProductsSiteView,
    'static': StaticViewSiteMap
}

from django.conf.urls import handler404, handler500

urlpatterns = [
    path('sitemap.xml',
         cache_page(86400)(sitemap), {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    url(r"^api-view/", include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    #SEKCJA STORE VIEW
    path('', StoreMainView.as_view(), name="store_view"),
    path('telefony-serwis-akcesoria/',
         StoreGsmMainView.as_view(),
         name="store_gsm_view"),
    path('grawerowanie-laserem-co2-oferta/',
         StoreGravMainView.as_view(),
         name="store_grav_view"),
    path('telefony-komorkowe-dostepne-w-sklepach-miktel-krakow-pulawy/',
         StoreGsmPhonesMainView.as_view(),
         name="store_gsm_phones_main_view"),
    path('telefon-komorkowy/<str:slug>/<int:id>',
         StoreGsmPhonesDetailsView.as_view(),
         name="store_gsm_phones_details_view"),
    path('serwis-telefonow-komorkowych-oferta-cennik/',
         StoreGsmSerwisMainView.as_view(),
         name="store_gsm_serwis_main_view"),
    path('serwis-telefonow-komorkowych-oferta-cennik/<str:slug>/<int:id>',
         StoreGsmItemsDetailsView.as_view(),
         name="store_gsm_item_details_view"),
    path('akcesoria-gsm-do-telefonow-komorkowych-oferta-cennik/',
         CategorysGSMView.as_view(),
         name="store_gsm_accessories_main_view"),
    path('grawerowanie-laserem-co2-kategorie/',
         CategorysGravView.as_view(),
         name="store_gsm_engraving_cat_view"),
    path('znakowanie-laserem-co2-kategorie/',
         CategorysGravMetalView.as_view(),
         name="store_gsm_engraving_metal_cat_view"),
    path('produkty/<str:cat>/<str:slug>/',
         CategorysView.as_view(),
         name="categorys"),
    path('produkty/<str:cat>/<str:slug>/<str:name>/<int:id>',
         ProductView.as_view(),
         name="products"),
    path('miktel/add_product/', AddProductView.as_view(), name="add_product"),
    path('miktel/add_factory/', AddFactoryView.as_view(), name="add_factory"),
    path('miktel/add_category/',
         AddCategoryView.as_view(),
         name="add_category"),

    #admin produktów
    path('miktel/products_list/',
         ProductsListView.as_view(),
         name="products_list"),
    path('miktel/add_images_product/<int:pk>',
         AddImagesProductView.as_view(),
         name="add_images_product"),
    path('miktel/update_image/<int:pk>',
         UpdateImageView.as_view(),
         name="update_image"),
    path('miktel/del_image/<int:pk>', DelImageView.as_view(),
         name="del_image"),
    path('miktel/update_product/<int:pk>',
         UpdateProductView.as_view(),
         name="update_product"),
    path('miktel/del_product/<int:pk>',
         DelProductView.as_view(),
         name="del_product"),
    path('miktel/add_foto_main/<int:pk>',
         AddMainFotoProductView.as_view(),
         name="add_foto"),
    path('miktel/update_category/',
         UpdateCategoryView.as_view(),
         name="update_category"),
    path('miktel/categorys_list/',
         CategoryListView.as_view(),
         name="categorys_list"),
    path('miktel/del_category/<int:pk>',
         DelCategoryView.as_view(),
         name="del_category"),
    path('miktel/add_foto_main_category/<int:pk>',
         AddMainFotoCategoryView.as_view(),
         name="add_foto_cat"),
    #Admin i main miktel
    path('admin/', admin.site.urls),
    path('miktel/', MainView.as_view(), name="widok_klienta"),
    #SEKCJA TELEFONY UMOWY I FAKTURY
    path('miktel/dodaj_telefon/',
         TelefonCreateView.as_view(),
         name="dodaj_telefon"),
    path('miktel/telefony_magazyn/',
         TelefonyMagazynView.as_view(),
         name="telefony_magazyn"),
    path('miktel/telefony_dostepne_magazyn/<int:pk>',
         TelefonyMagazynFilterView.as_view(),
         name="telefony_magazyn_filter"),
    path('miktel/add_phone_details/<int:pk>',
         PhoneDetailsView.as_view(),
         name="add_phone_details"),
    path('miktel/add_images_phones/<int:pk>',
         AddImagesPhoneView.as_view(),
         name="add_images_phone"),
    path('miktel/telefony_sprzedane_magazyn/<int:pk>',
         TelefonySprzedaneMagazynFilterView.as_view(),
         name="telefony_sprzedane_magazyn_filter"),
    path('miktel/add_info/<int:pk>',
         TelefonyMagazynInfoView.as_view(),
         name="telefony_info"),
    path('miktel/change_mag/<int:pk>',
         TelefonyMagazynChangeView.as_view(),
         name="change_mag"),
    path('miktel/sell_phones/<int:pk>',
         SellPhonesView.as_view(),
         name="sell_phone"),
    path('miktel/telefony_sprzedane/',
         TelefonySprzedaneView.as_view(),
         name="telefony_sprzedane"),
    path('miktel/telefony_zawieszone/',
         TelefonyZawieszoneView.as_view(),
         name="telefony_zawieszone"),
    path('miktel/reklamacja/<int:pk>',
         TelefonyReklamacjaView.as_view(),
         name="telefony_reklamacja"),
    path('miktel/wystaw_telefon/<int:pk>',
         WystawTelefonView.as_view(),
         name='wystaw_telefon'),
    path('miktel/szczegoly_telefonu/<int:pk>',
         SzczegolyTelefonuView.as_view(),
         name='szczegoly_telefonu'),
    path('miktel/umowa_komisowa/',
         UmowaKomisowaView.as_view(),
         name="umowa_komisowa"),
    path('miktel/lista_umow/', ListaUmowView.as_view(), name="lista_umow"),
    path('miktel/edycja_umowy/<int:pk>',
         EdycjaUmowyView.as_view(),
         name="edycja_umowy"),
    path('miktel/checking_document/',
         CheckingDocumentView.as_view(),
         name="checking_document/"),
    path('miktel/umowa_imei/<int:pk>',
         UmowaIdView.as_view(),
         name="umowa_imei"),
    path('miktel/faktura_imei/<int:pk>',
         FakturaIdView.as_view(),
         name="faktura_imei"),
    path('miktel/faktura_zakupu/',
         FakturaZakupuView.as_view(),
         name="faktura_zakupu"),
    path('miktel/checking_invoice/',
         CheckingInvoiceView.as_view(),
         name="checking_invoice"),
    path('miktel/lista_faktur/',
         ListaFakturView.as_view(),
         name="lista_faktur"),
    path('miktel/delete_invoice/<int:pk>',
         DeleteFakturaZakupuView.as_view(),
         name="delete_invoice"),
    path('miktel/edycja_faktury/<int:pk>',
         EdycjaFakturyView.as_view(),
         name="edycja_faktury"),
    path('miktel/wystaw_telefon/<int:pk>',
         WystawTelefonView.as_view(),
         name='wystaw_telefon'),

    #SEKCJA SERIWS I CZESCI
    path('miktel/dodaj_serwis/',
         DodajSerwisView.as_view(),
         name="dodaj_serwis"),
    path('miktel/szczegoly_serwisu/<int:pk>',
         SzczegolySerwisuView.as_view(),
         name='szczegoly_serwisu'),
    path('miktel/gotowy_do_odbioru/<int:pk>',
         GotowySerwisView.as_view(),
         name='gotowy_serwis'),
    path('miktel/wykonaj_serwis_z_czesciami/<int:pk>',
         GetServiceForItems.as_view(),
         name='wykonaj_serwis_z_czesciami'),
    path('miktel/save_service/<int:pk>',
         ServiceReadyView.as_view(),
         name='save_service'),
    path('miktel/wydaj_serwis/<int:pk>',
         WydajSerwisView.as_view(),
         name='wydaj_serwis'),
    path('miktel/wydaj_serwis_czesci/',
         WydajSerwisCzesciView.as_view(),
         name='wydaj_serwis_czesci'),
    path('miktel/wydaj_serwis_czesci2/',
         WydajSerwisCzesci2View.as_view(),
         name='wydaj_serwis_czesci2'),
    path('miktel/archiwum_serwisow/',
         ArchiwumSerwisView.as_view(),
         name='archiwum_serwisow'),
    path('miktel/reklamacja_serwis/<int:pk>',
         ReklamacjaSerwisView.as_view(),
         name='reklamacja_serwis'),
    path('miktel/lista_serwisow/',
         ListaSerwisowMagazynView.as_view(),
         name="lista_serwisow"),
    path('miktel/lista_serwisow/<int:pk>',
         ListaSerwisowFilterMagazynView.as_view(),
         name="lista_serwisow_filter"),
    path('miktel/lista_serwisow_gotowych/',
         ListaSerwisowGotowychMagazynView.as_view(),
         name="lista_serwisow_gotowych"),
    path('miktel/lista_serwisow_gotowych_filter/<int:pk>',
         ListaSerwisowGotowychFilterMagazynView.as_view(),
         name="lista_serwisow_gotowych_filter"),

    #SEKCJA PDF
    path('miktel/generuj_pdf/<int:pk>',
         GenerujPdfView.as_view(),
         name='pdf_umowa'),
    path('miktel/serwis_pdf/<int:pk>',
         DodajPDFSerwisView.as_view(),
         name="serwis_pdf"),

    #SEKCJA CZĘŚCI
    path('miktel/dodaj_czesc/', CzesciCreateView.as_view(),
         name='dodaj_czesc'),
    path('miktel/lista_czesci/',
         ListaCzesciView.as_view(),
         name='lista_czesci'),
    path('miktel/lista_czesci_miktel/',
         ListaCzesciAllView.as_view(),
         name='lista_czesci_all'),
    path('miktel/lista_czesci/<int:pk>',
         ListaCzesciLokalView.as_view(),
         name='lista_czesci_lokal'),
    path('miktel/szczegoly_czesci/<int:pk>',
         SzczegolyCzesciView.as_view(),
         name="szczegoly_czesci"),
    path('miktel/uzyj_czesci/',
         UzyjCzesciWieleView.as_view(),
         name="uzyj_czesci"),
    path('miktel/uzyj_czesci_serwis/',
         UzyjCzesciSerwisView.as_view(),
         name="uzyj_czesci_serwis"),
    path('miktel/usun_wiecej_czesci/<int:pk>',
         RemoveMoreItemsView.as_view(),
         name="usun_wiecej_czesci"),
    path('miktel/dodaj_wiecej_czesci/<int:pk>',
         AddMoreItemsView.as_view(),
         name="dodaj_wiecej_czesci"),
    path('miktel/dodaj_podobna_czesc/<int:pk>',
         AddMoreItemsSimiliarView.as_view(),
         name="dodaj_podobna_czesc"),

    #SEKCJA ADMINISTRACJI
    path('miktel/profil/<int:pk>', ProfilView.as_view(), name="profil"),
    path('miktel/payments/<int:pk>', PaymentsView.as_view(), name="payments"),
    path('miktel/work_schedule/',
         WorkScheduleView.as_view(),
         name="work_schedule"),
    path('miktel/del_work_schedule/<int:pk>',
         DeleteScheduleView.as_view(),
         name="del_work_schedule"),
    path('miktel/admin_payments/',
         AdminPaymentsView.as_view(),
         name="admin_payments"),
    path('miktel/add_payment/<int:pk>',
         AddPaymentView.as_view(),
         name="add_payment"),
    path('miktel/add_payment_adv/<int:pk>',
         AddPaymentAdvView.as_view(),
         name="add_payment_adv"),
    path('miktel/del_payment_adv/<int:pk>',
         DelPaymentAdvView.as_view(),
         name="del_payment_adv"),
    path('miktel/add_bonus/<int:pk>', AddBonusView.as_view(),
         name="add_bonus"),
    path('miktel/lista_uzytkownikow/',
         ListaMyUserView.as_view(),
         name="lista_uzytkownikow"),
    path('miktel/dodaj_uzytkownika/',
         DodajPracownikaView.as_view(),
         name="dodaj_uzytkownika"),
    path('miktel/edycja_uzytkownika/<int:pk>',
         EdycjaMyUserView.as_view(),
         name="edycja_uzytkownika"),
    path('miktel/lista_sklepow/',
         ListaSklepowView.as_view(),
         name="lista_sklepow"),
    path('miktel/edycja_sklepu/<int:pk>',
         EdycjaSklepuView.as_view(),
         name="edycja_sklepu"),
    path('miktel/dodaj_foto/', DodajFotoView.as_view(), name="dodaj_foto"),
    path('miktel/ustaw_foto/<int:pk>',
         UstawFotoProfilView.as_view(),
         name="ustaw_foto"),
    #     path('miktel/ustaw_page_records/',
    #          PageRecordsView.as_view(),
    #          name="ustaw_page_records"),
    path('miktel/ustaw_haslo/<int:pk>',
         UstawHasloView.as_view(),
         name="ustaw_haslo"),
    path('miktel/dodaj_sklep/', AddShopView.as_view(), name="dodaj_sklep"),
    path('miktel/dodaj_marke/', AddCompanyView.as_view(), name="dodaj_marke"),
    path('miktel/dodaj_typ/', AddTypeItemView.as_view(), name="dodaj_typ"),
    path('miktel/dodaj_adres/', AddAdresView.as_view(), name="dodaj_adres"),
    path('miktel/dodaj_hurtownie/',
         AddHurtowniaView.as_view(),
         name="dodaj_hurtownie"),
    path('miktel/dodaj_kategorie/',
         AddCategoryView.as_view(),
         name="dodaj_kategorie"),
    path('miktel/dodaj_inne/',
         DodajInnePraceView.as_view(),
         name='dodaj_inne_prace'),
    path('miktel/delete_document/<int:pk>',
         DeleteDocumentView.as_view(),
         name="delete_document"),
    path('miktel/lista_uslug/', ListaUslugView.as_view(), name="lista_uslug"),
    path('miktel/dodaj_usluge/',
         DodajUslugaView.as_view(),
         name="dodaj_usluge"),
    path('miktel/edycja_uslugi/<int:pk>',
         EdycjaUslugiView.as_view(),
         name="edycja_uslugi"),
    path('miktel/usun_usluge/<int:pk>',
         DeleteUslugaView.as_view(),
         name="usun_usluge"),

    #SECKJA PREMIOWANIE
    path('miktel/akcesoria_gsm_miesiąc/',
         DodajAkcesoriaView.as_view(),
         name="akcesoria_gsm_miesiąc/"),
    path('miktel/dashboard_sklepow/',
         DashboardView.as_view(),
         name="dashboard_sklepow"),
    path('miktel/dodaj_premiaJob/',
         DodajPremiaJobView.as_view(),
         name="dodaj_premiaJob"),
    path('miktel/twoje_premie/',
         TwojePremieJobView.as_view(),
         name="twoje_premieJob"),
    path('miktel/edycja_premiaJob/<int:pk>',
         EdycjaPremiaJobView.as_view(),
         name="edycja_premiaJob"),
    path(
        'miktel/szczegoly_serwisow_serwisanta/<int:pk>/<int:miesiac>/<int:rok>/',
        SzczegolySerwisySerwisantaView.as_view(),
        name='szczegoly_serwisow_serwisanta'),
    path('miktel/login/', UserLoginView.as_view(), name="login"),
    path('miktel/logout/', User_Logout),
    url(
        r'^robots\.txt$',
        TemplateView.as_view(template_name="miktel/robots.txt",
                             content_type='text/plain')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [] + static(settings.STATIC_URL,
                           document_root=settings.STATIC_ROOT)

handler404 = error404
handler404 = error500