from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from miktel.models import Telefon, Sklep, Adres, Foto
from miktel.function import send_email
from store.forms import *
from django.contrib import messages

from django.views import View
from django.db.models import Q
from functools import reduce
from operator import countOf, or_, and_
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
# Create your views here.
from django.utils.text import slugify

import warnings
import django

import os
from django.core.mail import send_mail
from django.conf import settings

from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache.utils import make_template_fragment_key
from django.views.decorators.csrf import csrf_protect

from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()

    for kwarg in kwargs:
        try:
            query.pop(kwarg)
        except KeyError:
            pass

    query.update(kwargs)

    return mark_safe(query.urlencode())


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class CacheMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(
            CacheMixin, self).dispatch)(*args, **kwargs)


class StoreMainView(View):
    def get(self, request):
        cookie_law = request.COOKIES.get('cookielaw_accepted')
        response = HttpResponse()
        response.delete_cookie('cookielaw_accepted')
        articles = Articles.objects.filter(site_id=1)
        shop = Sklep.objects.all().first()
        ctx = {'articles': articles, 'shop': shop}
        return TemplateResponse(request, "store.html", ctx)


class StoreGsmMainView(View):
    def get(self, request):
        articles = Articles.objects.filter(site_id=2)
        # cookie_law = request.COOKIES.get('cookielaw_accepted')
        phones_mark = Marka.objects.filter(gsm=True)
        accessories_factory = Factory.objects.filter(accessories=True)
        ctx = {
            'articles': articles,
            'phones_mark': phones_mark,
            'accessories_factory': accessories_factory
        }
        return TemplateResponse(request, "store_gsm.html", ctx)

    def post(self, request):
        send_email = "Wysłano email"
        ctx = {'send_email': send_email}
        return TemplateResponse(request, "store_gsm.html", ctx)


class StoreGravMainView(View):
    def get(self, request):
        articles = Articles.objects.filter(site_id=3)
        ctx = {'articles': articles}
        return TemplateResponse(request, "store_grav.html", ctx)

    def post(self, request):
        send_email = "Wysłano email"
        ctx = {'send_email': send_email}
        return TemplateResponse(request, "store_grav.html", ctx)


class StoreStampMainView(View):
    def get(self, request):
        articles = Articles.objects.filter(site_id=4)
        ctx = {'articles': articles}
        return TemplateResponse(request, "store_stamp.html", ctx)

    def post(self, request):
        send_email = "Wysłano email"
        ctx = {'send_email': send_email}
        return TemplateResponse(request, "store_stamp.html", ctx)


class StoreKeysMainView(View):
    def get(self, request):
        articles = Articles.objects.filter(site_id=5)
        ctx = {'articles': articles}
        return TemplateResponse(request, "store_keys.html", ctx)

    def post(self, request):
        send_email = "Wysłano email"
        ctx = {'send_email': send_email}
        return TemplateResponse(request, "store_keys.html", ctx)


# @cache_page(CACHE_TTL)
# @method_decorator(cache_page, name='dispatch')
# @cache_page(60 * 15)
class StoreGsmPhonesMainView(View):
    def get(self, request):
        promo = request.GET.get('promo')
        category = request.GET.get('category')
        mark = request.GET.get('mark')
        shop = request.GET.get('shops')
        price_start = request.GET.get('price_start')
        price_end = request.GET.get('price_end')
        phones = Telefon.objects.filter(
            dostepny=True).filter(
            zawieszony=False).order_by(
            'marka', 'nazwa', 'cena_sprzed')

        phones_counter = phones.count()
        new_phones_counter = phones.filter(stan=0).count()
        used_phones_counter = phones.filter(stan=1).count()
        most_mark = phones.values('marka').annotate(
            total=Count('marka')).order_by('-total')[0:5]
        m = []
        for el in most_mark:
            marks = Marka.objects.get(pk=el['marka'])
            total = (el['total'])
            dict_most = {'marka': marks, 'total': total}
            m.append(dict_most)

        most_category = phones.values('kategoria').annotate(
            total=Count('kategoria')).order_by('-total')[0:5]
        c = []
        for el in most_category:
            cat = Kategoria.objects.get(pk=el['kategoria'])
            total = (el['total'])
            dict_cats = {'cat': cat, 'total': total}
            c.append(dict_cats)
        phones =  Telefon.objects.filter(
            dostepny=True).filter(
            zawieszony=False).order_by(
            'marka', 'nazwa', 'cena_sprzed')

        if promo == "on":
            phones = phones.filter(in_promo=True)

        if shop != "":
            phones = phones.filter(magazyn_aktualny=shop)

        if mark != "":
            phones = phones.filter(marka=mark)
        if category != '':
            phones = phones.filter(kategoria=category)

        if price_start:
            price_start = price_start
        else:
            price_start = 0.0
        phones = phones.filter(
            cena_sprzed__gte=price_start).order_by('cena_sprzed')
        if price_end != "":
            if price_end != None:
                price_end = price_end
            else:
                price_end = 10000.0
        else:
            price_end = 10000.0
        phones = phones.filter(
            cena_sprzed__lte=price_end).order_by('cena_sprzed')

        if shop == None or mark == None or category == None:
            phones =  Telefon.objects.filter(
            dostepny=True).filter(
            zawieszony=False).order_by(
            'marka', 'nazwa', 'cena_sprzed')
        page = request.GET.get('page')
        page_records = 20
        paginator = Paginator(phones, page_records)
        phones_pagi = paginator.get_page(page)
        form_filter = FilterForm()

        ctx = {
            "products": phones_pagi,
            "price_start": price_start,
            "price_end": price_end,
            "products_counter": phones_counter,
            "new_products_counter": new_phones_counter,
            "used_products_counter": used_phones_counter,
            "most_mark": m,
            "most_cats": c,
            "page_records": phones,
            "paginator": paginator,
            "form_filter": form_filter,
        }
        # return render('telefony-komorkowe-dostepne-w-sklepach-miktel')
        return TemplateResponse(request, "store_gsm_phones.html", ctx)


class StoreGsmPhonesSearchView(View):
    def get(self, request):
        search = request.GET.get('search')
        phones = Telefon.objects.filter(dostepny=True).order_by(
            'marka', 'nazwa', 'cena_sprzed')
        phones_counter = phones.count()
        new_phones_counter = phones.filter(stan=0).count()
        used_phones_counter = phones.filter(stan=1).count()
        most_mark = phones.values('marka').annotate(
            total=Count('marka')).order_by('-total')[0:5]
        m = []
        for el in most_mark:
            marks = Marka.objects.get(pk=el['marka'])
            total = (el['total'])
            dict_most = {'marka': marks, 'total': total}
            m.append(dict_most)

        most_category = phones.values('kategoria').annotate(
            total=Count('kategoria')).order_by('-total')[0:5]
        c = []
        for el in most_category:
            cat = Kategoria.objects.get(pk=el['kategoria'])
            total = (el['total'])
            dict_cats = {'cat': cat, 'total': total}
            c.append(dict_cats)
        phones = Telefon.objects.filter(dostepny=True).order_by(
            'marka', 'nazwa', 'cena_sprzed')
        search_d = search.split(" ")
        search_d = list(search_d)
        q_object = reduce(and_, (Q(nazwa__icontains=search_d)
                                 | Q(marka__nazwa__icontains=search_d)
                                 | Q(kategoria__nazwa__icontains=search_d)
                                 for search_d in search_d))
        phones = Telefon.objects.filter(q_object).filter(
            dostepny=True).order_by('marka', 'nazwa', 'cena_sprzed')
        page = request.GET.get('page')
        page_records = 20
        paginator = Paginator(phones, page_records)
        phones_pagi = paginator.get_page(page)
        form_filter = FilterForm()
        ctx = {
            "products": phones_pagi,
            "products_counter": phones_counter,
            "new_products_counter": new_phones_counter,
            "used_products_counter": used_phones_counter,
            "most_mark": m,
            "most_cats": c,
            "page_records": phones,
            "paginator": paginator,
            "form_filter": form_filter,
        }
        return TemplateResponse(request, "store_gsm_phones.html", ctx)


class StoreGsmPhonesDetailsView(View):
    def get(self, request, slug, id):
        # phone = Telefon.objects.get(pk=id)
        phone = get_object_or_404(Telefon, slug=slug, id=id)
        fotos = FotoProduct.objects.filter(phone_id=phone.id).order_by('id')
        fotos_mix = {}
        i = 0
        for i in range(len(fotos)):
            if fotos[i].another_min == True:
                fotos_mix.update({fotos[i]: fotos[i - 1]})
        details = ProductDetails.objects.filter(phone_id=phone.id)
        foto_count = fotos.count()
        if foto_count > 1:
            foto_count = foto_count / 2
        ctx = {
            "phone": phone,
            "details": details,
            "fotos": fotos,
            "fotos_mix": fotos_mix,
            'foto_count': foto_count
        }
        return TemplateResponse(request, "store_gsm_phone_details.html", ctx)

    def post(self, request, slug, id):
        if 'ask_for' in request.POST:
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            text = request.POST.get("text")
            text += "\n" + "Temat emaila" + str(
                subject) + "\n" + "Email kontaktowy - " + str(email)
            # send_email(subject, text)
            send_mail(subject, text, settings.EMAIL_HOST_USER,
                      [settings.EMAIL_HOST_USER])
            return redirect('store_gsm_phones_main_view')


class StoreGsmSerwisMainView(View):
    def get(self, request):
        items = Czesc.objects.all()
        form_filter = FilterSerwisForm()
        items_instock = items.filter(dostepny=True)
        items_instock_count = items_instock.count()
        services = DodajSerwis.objects.all()
        services_arch = services.filter(archiwum=True)
        services_arch_count = services.count()
        most_mark = items.values('marka').annotate(
            total=Count('marka')).order_by('-total')[0:5]
        m = []
        for el in most_mark:
            marka = Marka.objects.get(pk=el['marka'])
            total = (el['total'])
            dict_most = {'marka': marka, 'total': total}
            m.append(dict_most)

        most_category = items.values('typ').annotate(
            total=Count('typ')).order_by('-total')[0:5]
        c = []

        for el in most_category:
            typ = Typ.objects.get(pk=el['typ'])
            total = (el['total'])
            dict_cats = {'cat': typ, 'total': total}
            c.append(dict_cats)

        promo = request.GET.get('promo')
        typ = request.GET.get('typ')
        mark = request.GET.get('mark')
        shop = request.GET.get('shops')
        price_start = request.GET.get('price_start')
        price_end = request.GET.get('price_end')

        if promo == "on":
            items = items.filter(in_promo=True)
        if shop != "":
            items = items.filter(sklep=shop).order_by('marka')
        if mark != "":
            items = items.filter(marka=mark).order_by('marka')
        if typ != '':
            items = items.filter(typ=typ).order_by('marka')
        if price_start != None:
            price_start = price_start
        else:
            price_start = 0.0
        if price_end != None:
            price_end = price_end
        else:
            price_end = 10000.0
            items = items.filter(cena_sprzed__gte=price_start).filter(
                cena_sprzed__lte=price_end).order_by('cena_sprzed')
        if mark == None:
            items = Czesc.objects.all().order_by('marka').order_by(
                'nazwa').order_by('typ')

        page = request.GET.get('page')
        page_records = 20
        items = items.order_by('marka', 'nazwa', 'typ')
        paginator = Paginator(items, page_records)
        items_pagi = paginator.get_page(page)
        form_filter = FilterSerwisForm()
        ctx = {
            "products": items_pagi,
            "products_counter": items_instock_count,
            "services": services,
            "services_arch": services_arch,
            "services_arch_count": services_arch_count,
            "most_mark": m,
            "most_cats": c,
            "page_records": page_records,
            "paginator": paginator,
            "form_filter": form_filter,
        }
        return TemplateResponse(request, "store_gsm_serwis.html", ctx)


class StoreGsmSerwisSearchView(View):
    def get(self, request):
        search = request.GET.get('search')
        items = Czesc.objects.all()
        form_filter = FilterSerwisForm()
        items_instock = items.filter(dostepny=True)
        items_instock_count = items_instock.count()
        services = DodajSerwis.objects.all()
        services_arch = services.filter(archiwum=True)
        services_arch_count = services.count()
        most_mark = items.values('marka').annotate(
            total=Count('marka')).order_by('-total')[0:5]
        m = []
        for el in most_mark:
            marka = Marka.objects.get(pk=el['marka'])
            total = (el['total'])
            dict_most = {'marka': marka, 'total': total}
            m.append(dict_most)

        most_category = items.values('typ').annotate(
            total=Count('typ')).order_by('-total')[0:5]
        c = []

        for el in most_category:
            typ = Typ.objects.get(pk=el['typ'])
            total = (el['total'])
            dict_cats = {'cat': typ, 'total': total}
            c.append(dict_cats)
        search_d = search.split(" ")
        search_d = list(search_d)
        items = Czesc.objects.all()
        q_object = reduce(and_, (Q(nazwa__icontains=search_d)
                                 | Q(marka__nazwa__icontains=search_d)
                                 | Q(typ__nazwa__icontains=search_d)
                                 for search_d in search_d))
        items = Czesc.objects.filter(q_object)
        page = request.GET.get('page')
        page_records = 20
        paginator = Paginator(items, page_records)
        items_pagi = paginator.get_page(page)
        form_filter = FilterSerwisForm()

        ctx = {
            "products": items_pagi,
            "products_counter": items_instock_count,
            "services": services,
            "services_arch": services_arch,
            "services_arch_count": services_arch_count,
            "most_mark": m,
            "most_cats": c,
            "page_records": page_records,
            "paginator": paginator,
            "form_filter": form_filter,
        }
        return TemplateResponse(request, "store_gsm_serwis.html", ctx)


class StoreGsmItemsDetailsView(View):
    def get(self, request, slug, id):
        item = Czesc.objects.get(pk=id)

        fotos = FotoProduct.objects.filter(item_id=item.id).order_by('id')
        fotos_mix = {}
        i = 0
        for i in range(len(fotos)):
            if fotos[i].another_min == True:
                fotos_mix.update({fotos[i]: fotos[i - 1]})
        details = ProductDetails.objects.filter(item_id=item.id)
        foto_count = fotos.count()
        if foto_count > 1:
            foto_count = foto_count / 2
        ctx = {
            "product": item,
            "details": details,
            "fotos": fotos,
            "fotos_mix": fotos_mix,
            'foto_count': foto_count
        }
        return TemplateResponse(request, "store_gsm_serwis_details.html", ctx)

    def post(self, request, slug, id):
        if 'ask_for' in request.POST:
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            text = request.POST.get("text")
            text += "\n" + "Temat emaila" + str(
                subject) + "\n" + "Email kontaktowy - " + str(email)
            # send_email(subject, text)
            send_mail(subject, text, settings.EMAIL_HOST_USER,
                      [settings.EMAIL_HOST_USER])
            return redirect('store_gsm_serwis_main_view')


class CategorysGSMView(View):
    def get(self, request):
        mark = request.GET.get('mark')
        if mark == None:
            accessories_cats = Categorys.objects.filter(profile_id=1)
            ctx = {"accessories_cats": accessories_cats}
            return TemplateResponse(request, "store_gsm_categorys_main.html",
                                    ctx)
        else:
            profile = Profile.objects.get(pk=1)
            products = Products.objects.filter(factory_id=mark)
            prod_count = products.count()
            mark = Factory.objects.get(pk=mark)
            ctx = {
                "profile": profile,
                "products": products,
                "prod_count": prod_count,
                'mark': mark,
            }
            return TemplateResponse(request,
                                    "store_gsm_categorys_by_cat_mark.html",
                                    ctx)


class CategorysGSMSearchView(View):
    def get(self, request):
        search = request.GET.get('search')
        accessories_cats = Categorys.objects.filter(profile_id=1).filter(
            name__icontains=search)
        ctx = {"accessories_cats": accessories_cats}
        return TemplateResponse(request, "store_gsm_categorys_main.html", ctx)


class CategorysGravView(View):
    def get(self, request):
        cats = Categorys.objects.filter(profile_id=2)
        profile = Profile.objects.get(pk=2)
        ctx = {"profile": profile, "cats": cats}
        return TemplateResponse(request, "store_grav_categorys_main.html", ctx)


class CategorysGravMetalView(View):
    def get(self, request):
        cats = Categorys.objects.filter(profile_id=3)
        profile = Profile.objects.get(pk=3)
        print('hello1')
        ctx = {"profile": profile, "cats": cats}
        return TemplateResponse(request,
                                "store_grav_metal_categorys_main.html", ctx)


class CategorysView(View):
    def get(
        self,
        request,
        cat,
        slug,
    ):
        cat = Categorys.objects.get(slug=slug)
        products = Products.objects.filter(category_id=cat).order_by('name')
        profile = Profile.objects.get(pk=cat.profile_id.id)
        articles = Articles.objects.filter(category_id=cat)
        prod_count = products.count()
        ctx = {
            "profile": profile,
            "products": products,
            "cat": cat,
            "prod_count": prod_count,
            'articles': articles
        }
        if cat.profile_id.id == 1:
            return TemplateResponse(request,
                                    "store_gsm_categorys_by_cat_filter.html",
                                    ctx)
        if cat.profile_id.id == 2 or cat.profile_id.id == 3:
            return TemplateResponse(request,
                                    "store_grav_categorys_by_cat_filter.html",
                                    ctx)
        if cat.profile_id.id == 4:
            return TemplateResponse(
                request, "store_stamp_categorys_by_cat_filter.html", ctx)
        if cat.profile_id.id == 5:
            return TemplateResponse(request,
                                    "store_keys_categorys_by_cat_filter.html",
                                    ctx)

    def post(self, request, slug, id):
        if 'ask_for' in request.POST:
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            text = request.POST.get("text")
            text += "\n" + "Temat emaila" + str(
                subject) + "\n" + "Email kontaktowy - " + str(email)
            # send_email(subject, text)
            send_mail(subject, text, settings.EMAIL_HOST_USER,
                      [settings.EMAIL_HOST_USER])
            return redirect('accessories')


class StoreGravSearchView(View):
    def get(self, request):
        search = request.GET.get('search')
        cats = Categorys.objects.filter(profile_id__in=[2, 3]).filter(
            name__icontains=search)
        products = Products.objects.filter(category_id__in=cats)
        prod_count = products.count()
        ctx = {"products": products, 'prod_count': prod_count}
        return TemplateResponse(request,
                                "store_grav_categorys_by_cat_filter.html", ctx)


class StoreStampSearchView(View):
    def get(self, request):
        search = request.GET.get('search')
        cats = Categorys.objects.filter(profile_id=4).filter(
            name__icontains=search)
        products = Products.objects.filter(category_id__in=cats)
        prod_count = products.count()
        ctx = {"products": products, 'prod_count': prod_count}
        return TemplateResponse(request,
                                "store_stamp_categorys_by_cat_filter.html",
                                ctx)


class StoreKeysSearchView(View):
    def get(self, request):
        search = request.GET.get('search')
        cats = Categorys.objects.filter(profile_id=4).filter(
            name__icontains=search)
        products = Products.objects.filter(category_id__in=cats)
        prod_count = products.count()
        ctx = {"products": products, 'prod_count': prod_count}
        return TemplateResponse(request,
                                "store_keys_categorys_by_cat_filter.html", ctx)


class CategorysAutoMarksView(View):
    def get(self, request):
        marks = Marka.objects.filter(keys=True)
        marks_count = marks.count()
        profile = Profile.objects.get(pk=4)
        ctx = {'marks': marks, 'profile': profile, 'marks_count': marks_count}
        return TemplateResponse(request, "store_keys_auto_categorys_main.html",
                                ctx)


class CategorysAutoKeysMarkView(View):
    def get(self, request, mark):
        mark = Marka.objects.get(slug=mark)
        products = Products.objects.filter(mark_id=mark)
        products_count = products.count()
        profile = Profile.objects.get(pk=5)
        ctx = {
            "profile": profile,
            "products": products,
            'products_count': products_count,
            'mark': mark,
        }
        return TemplateResponse(
            request, "store_keys_auto_categorys_by_cat_filter.html", ctx)


#         if mark == None:
#             accessories_cats = Categorys.objects.filter(profile_id=4)
#             ctx = {"accessories_cats": accessories_cats}
#             return TemplateResponse(request,
#                                     "store_keys_categorys_by_cat_filter.html",
#                                     ctx)
#         else:
#
#             products = Products.objects.filter(factory_id=mark)
#             prod_count = products.count()
#             mark = Factory.objects.get(pk=mark)
#             ctx = {
#                 "profile": profile,
#                 "products": products,
#                 "prod_count": prod_count,
#                 'mark': mark,
#             }
#

# class CategorysAutoKeysSearchView(View):
#     def get(self, request):
#         search = request.GET.get('search')
#         accessories_cats = Categorys.objects.filter(profile_id=1).filter(
#             name__icontains=search)
#         ctx = {"accessories_cats": accessories_cats}
#         return TemplateResponse(request, "store_gsm_categorys_main.html", ctx)


class ProductView(View):
    def get(self, request, cat, slug, name, id):
        cat = Categorys.objects.get(slug=slug)
        product = Products.objects.get(id=id)
        fotos = FotoProduct.objects.filter(
            product_id=product.id).order_by('id')
        fotos_mix = {}
        i = 0
        for i in range(len(fotos)):
            if fotos[i].another_min == True:
                fotos_mix.update({fotos[i]: fotos[i - 1]})
        send_email = False
        foto_count = fotos.filter(another=True).count()
        # if foto_count > 1:
        #     foto_count = (foto_count / 2)
        #     foto_count = int(foto_count)
        #     # foto_count = round(foto_count, 0)
        ctx = {
            "send_email": send_email,
            "fotos_mix": fotos_mix,
            "product": product,
            "cat": cat,
            'foto_count': foto_count
        }
        if cat.profile_id.id == 1:
            return TemplateResponse(request, "store_product_gsm_details.html",
                                    ctx)
        if cat.profile_id.id == 2 or cat.profile_id.id == 3:
            return TemplateResponse(request, "store_product_grav_details.html",
                                    ctx)
        if cat.profile_id.id == 4:
            return TemplateResponse(request,
                                    "store_product_stamp_details.html", ctx)
        if cat.profile_id.id == 5:
            if product.mark_id != None:
                if product.mark_id.keys == True:
                    return TemplateResponse(
                        request, "store_product_keys_auto_details.html", ctx)
                else:
                    return TemplateResponse(request,
                                            "store_product_keys_details.html",
                                            ctx)
            return TemplateResponse(request, "store_product_keys_details.html",
                                    ctx)

    def post(self, request, cat, slug, name, id):
        if 'ask_for' in request.POST:
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            text = request.POST.get("text")
            text += "\n" + "Temat emaila" + str(
                subject) + "\n" + "Email kontaktowy - " + str(email)
            # send_email(subject, text)
            send_mail(subject, text, settings.EMAIL_HOST_USER,
                      [settings.EMAIL_HOST_USER])
            cat = Categorys.objects.get(slug=slug)
            product = Products.objects.get(id=id)
            fotos = FotoProduct.objects.filter(
                product_id=product.id).order_by('id')
            fotos_mix = {}
            i = 0
            for i in range(len(fotos)):
                if fotos[i].another_min == True:
                    fotos_mix.update({fotos[i]: fotos[i - 1]})
            send_email = True
            ctx = {
                "send_email": send_email,
                "fotos_mix": fotos_mix,
                "product": product,
                "cat": cat,
            }
            if cat.profile_id.id == 1:
                return TemplateResponse(request,
                                        "store_product_gsm_details.html", ctx)
            if cat.profile_id.id == 2 or cat.profile_id.id == 3:
                return TemplateResponse(request,
                                        "store_product_grav_details.html", ctx)
            if cat.profile_id.id == 4:
                return TemplateResponse(request,
                                        "store_product_stamp_details.html",
                                        ctx)
            if cat.profile_id.id == 5:
                return TemplateResponse(request,
                                        "store_product_keys_details.html", ctx)
                return redirect('store_gsm_serwis_main_view')


class ContactView(View):
    def get(self, request, slug):
        shop = Sklep.objects.get(slug=slug)
        profiles = Profile.objects.all().order_by('name')
        reCapForm = ReCAPTCHAForm()
        ctx = {'profiles': profiles, 'shop': shop, 'reCapForm': reCapForm}
        return TemplateResponse(request, "store_contact_us.html", ctx)

    def post(self, request, slug):
        shop = Sklep.objects.get(slug=slug)
        if 'ask_for' in request.POST:
            reCapForm = ReCAPTCHAForm(request.POST)
            if reCapForm.is_valid():
                email = request.POST.get("email")
                subject = request.POST.get("subject")
                text = request.POST.get("text")
                counter = request.POST.get("counter")
                if subject != '-1' and subject != '-2':
                    subject = Profile.objects.get(pk=int(subject))
                    subject = subject.name
                    text += "\n" + "Temat emaila : " + str(
                        subject) + "\n" + "Email kontaktowy - " + str(
                            email) + "\n" + "Kontakt do " + str(shop)
                elif subject == '-2':
                    subject = "Dział inne"
                    text += "\n" + "Temat emaila : " + str(
                        subject) + "\n" + "Email kontaktowy - " + str(
                            email) + "\n" + "Kontakt do " + str(shop)
                else:
                    subject = 'Brak wybranego działu'
                    text += "\n" + "Temat emaila : " + str(
                        subject) + "\n" + "Email kontaktowy - " + str(
                            email) + "\n" + "Kontakt do " + str(shop)
                if int(counter) > 10:
                    send_mail(subject, text, settings.EMAIL_HOST_USER,
                            [settings.EMAIL_HOST_USER])
                    messages.success(request,
                                    'Wysysłanie email zakończnono poprawnie.')
                else:
                    print('Not OK')
                    messages.error(request,
                                    'Wysysłanie email zbyt szybko. Chyba jesteś robotem?.')
            else:
                messages.error(request,
                               'Wystąpił błąd podczas wypełniana formularza.')
            return redirect('contact_page', slug=shop.slug)


class CookiesView(View):
    def get(self, request):
        return TemplateResponse(request, "cookies.html")


def error404(request, *args):
    return render(request, '404.html')


def error500(request, *args):
    return render(request, '500.html')
