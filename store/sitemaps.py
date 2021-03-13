from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from miktel.models import Telefon, Czesc, Products, Categorys, Sklep, Marka


class PhoneSiteView(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return Telefon.objects.filter(dostepny=True)


class PhoneMainSiteView(Sitemap):
    def items(self):
        return ['store_gsm_phones_main_view']

    def location(self, items):
        return reverse(items)


class PhoneSearchSiteView(Sitemap):
    def items(self):
        return ['store_gsm_phones_search_view']

    def location(self, items):
        return reverse(items)


class ItemsSiteView(Sitemap):
    def items(self):
        return Czesc.objects.all()


class ItemMainSiteView(Sitemap):
    def items(self):
        return ['store_gsm_serwis_main_view']

    def location(self, items):
        return reverse(items)


class ItemSearchSiteView(Sitemap):
    def items(self):
        return ['store_gsm_serwis_search_view']

    def location(self, items):
        return reverse(items)


class CategorysGSMSiteView(Sitemap):
    def items(self):
        # return ['categorys']
        return Categorys.objects.all()


class CategorysAutoMarkSiteView(Sitemap):
    def items(self):
        # return ['categorys']
        return Marka.objects.filter(keys=True)


class ProductsSiteView(Sitemap):
    def items(self):
        return Products.objects.all()


class ContactSiteView(Sitemap):
    def items(self):
        return Sklep.objects.filter(serwis_zew=False)


class StaticViewSiteMap(Sitemap):
    def items(self):
        return [
            'store_view', 'store_gsm_view', 'store_grav_view',
            'store_keys_view', 'auto-marks', 'store_stamp_view',
            'store_gsm_phones_main_view', 'store_gsm_serwis_main_view',
            'store_gsm_accessories_main_view',
            'store_gsm_engraving_metal_cat_view', 'cookies'
        ]

    def location(self, items):
        return reverse(items)
