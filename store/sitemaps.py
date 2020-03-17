from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from miktel.models import Telefon, Czesc, Products, Categorys


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


class ItemsSiteView(Sitemap):
    def items(self):
        return Czesc.objects.all()

    # def items(self):
    #     return ['accessories']

    # def location(self, items):
    #     return reverse(items)


class ItemMainSiteView(Sitemap):
    def items(self):
        return ['store_gsm_serwis_main_view']

    def location(self, items):
        return reverse(items)


class CategorysGSMSiteView(Sitemap):
    def items(self):
        # return ['categorys']
        return Categorys.objects.all()

    # def location(self, items):
    #     return reverse(items)


class ProductsSiteView(Sitemap):
    def items(self):
        return Products.objects.all()


class StaticViewSiteMap(Sitemap):
    def items(self):
        return [
            'store_view', 'store_gsm_view', 'store_grav_view',
            'store_gsm_phones_main_view', 'store_gsm_serwis_main_view',
            'store_gsm_accessories_main_view',
            'store_gsm_engraving_metal_cat_view'
        ]

    def location(self, items):
        return reverse(items)
