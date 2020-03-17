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
from operator import or_
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
# Create your views here.
from django.utils.text import slugify


class StoreMainView(View):
    def get(self, request):
        return TemplateResponse(request, "store.html")


class StoreGsmMainView(View):
    def get(self, request):
        return TemplateResponse(request, "store_gsm.html")

    def post(self, request):
        send_email = "Wysłano email"
        ctx = {'send_email': send_email}
        return TemplateResponse(request, "store_gsm.html", ctx)


class StoreGravMainView(View):
    def get(self, request):
        return TemplateResponse(request, "store_grav.html")

    def post(self, request):
        send_email = "Wysłano email"
        ctx = {'send_email': send_email}
        return TemplateResponse(request, "store_grav.html", ctx)


class StoreGsmPhonesMainView(View):
    def get(self, request):
        phones = Telefon.objects.filter(dostepny=True).order_by(
            'marka', 'nazwa', 'cena_sprzed')
        phones_counter = phones.count()
        new_phones_counter = phones.filter(stan=0).count()
        used_phones_counter = phones.filter(stan=1).count()
        most_mark = phones.values('marka').annotate(
            total=Count('marka')).order_by('-total')[0:5]
        m = []
        for el in most_mark:
            marka = Marka.objects.get(pk=el['marka'])
            total = (el['total'])
            dict_most = {'marka': marka, 'total': total}
            m.append(dict_most)

        most_category = phones.values('kategoria').annotate(
            total=Count('kategoria')).order_by('-total')[0:5]
        c = []
        for el in most_category:
            category = Kategoria.objects.get(pk=el['kategoria'])
            total = (el['total'])
            dict_cats = {'cat': category, 'total': total}
            c.append(dict_cats)
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
            "page_records": page_records,
            "paginator": paginator,
            "form_filter": form_filter,
        }
        return TemplateResponse(request, "store_gsm_phones.html", ctx)

    def post(self, request):
        form_filter = FilterForm(request.POST)
        phones = Telefon.objects.filter(dostepny=True).order_by(
            'marka', 'nazwa', 'cena_sprzed')

        if form_filter.is_valid():
            shops = form_filter.cleaned_data['shops']
            mark = form_filter.cleaned_data['mark']
            category = form_filter.cleaned_data['category']
            price_start = form_filter.cleaned_data['price_start']
            price_end = form_filter.cleaned_data['price_end']
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
            if shops != None:
                phones = phones.filter(magazyn_aktualny=shops)
            if mark != None:
                phones = phones.filter(marka=mark)
            if category != None:
                phones = phones.filter(kategoria=category)
            if price_start != None:
                price_start = price_start
            else:
                price_start = 0.0
            if price_end != None:
                price_end = price_end
            else:
                price_end = 10000.0

            phones = phones.filter(cena_sprzed__gte=price_start).filter(
                cena_sprzed__lte=price_end).order_by('cena_sprzed')
            page = request.POST.get('page')
            page_records = 40
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
                "page_records": page_records,
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
        # for el in details:
        #     print(el)

        ctx = {
            "phone": phone,
            "details": details,
            "fotos": fotos,
            "fotos_mix": fotos_mix
        }
        return TemplateResponse(request, "store_gsm_phone_details.html", ctx)

    def post(self, request, slug, id):
        if 'ask_for' in request.POST:
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            text = request.POST.get("text")
            text += "\n" + "Temat emaila" + str(
                subject) + "\n" + "Email kontaktowy - " + str(email)
            send_email(subject, text)
            return redirect('store_gsm_phones_main_view')


class StoreGsmSerwisMainView(View):
    def get(self, request):
        items = Czesc.objects.all()
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
        page = request.GET.get('page')
        page_records = 40
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

    def post(self, request):
        items = Czesc.objects.all()
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
            page = request.GET.get('page')

        if "search" in request.POST:
            search = request.POST.get("search")
            search_d = search.split(" ")
            search_d = list(search_d)
            print(search_d)
            items = Czesc.objects.all()
            q_object = reduce(or_, (Q(nazwa__icontains=search_d)
                                    | Q(marka__nazwa__icontains=search_d)
                                    for search_d in search_d))
            items = Czesc.objects.filter(q_object)

            page_records = 40
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

        form_filter = FilterSerwisForm(request.POST)
        if form_filter.is_valid():
            shops = form_filter.cleaned_data['shops']
            mark = form_filter.cleaned_data['mark']
            typ = form_filter.cleaned_data['typ']

            if shops != None:
                items = items.filter(sklep=shops)
            if mark != None:
                items = items.filter(marka=mark)
            if typ != None:
                items = items.filter(typ=typ)

            page = request.POST.get('page')
            page_records = 40
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
        else:
            return redirect('store_gsm_serwis_main_view')


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

        ctx = {
            "product": item,
            "details": details,
            "fotos": fotos,
            "fotos_mix": fotos_mix
        }
        return TemplateResponse(request, "store_gsm_serwis_details.html", ctx)

    def post(self, request, slug, id):
        if 'ask_for' in request.POST:
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            text = request.POST.get("text")
            text += "\n" + "Temat emaila" + str(
                subject) + "\n" + "Email kontaktowy - " + str(email)
            send_email(subject, text)
            return redirect('store_gsm_serwis_main_view')


class CategorysGSMView(View):
    def get(self, request):
        accessories_cats = Categorys.objects.filter(accessories=True)
        ctx = {"accessories_cats": accessories_cats}
        return TemplateResponse(request, "store_gsm_categorys_main.html", ctx)


class CategorysGravView(View):
    def get(self, request):
        cats = Categorys.objects.filter(profile_id=2)
        profile = Profile.objects.get(pk=2)
        print('hello1')
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
        print(profile)
        prod_count = products.count()
        ctx = {
            "profile": profile,
            "products": products,
            "cat": cat,
            "prod_count": prod_count
        }
        if cat.profile_id.id == 1:
            return TemplateResponse(request,
                                    "store_gsm_categorys_by_cat_filter.html",
                                    ctx)
        if cat.profile_id.id == 2 or cat.profile_id.id == 3:
            return TemplateResponse(request,
                                    "store_grav_categorys_by_cat_filter.html",
                                    ctx)

    def post(self, request, slug, id):
        if 'ask_for' in request.POST:
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            text = request.POST.get("text")
            text += "\n" + "Temat emaila" + str(
                subject) + "\n" + "Email kontaktowy - " + str(email)
            send_email(subject, text)
            return redirect('accessories')


class ProductView(View):
    def get(self, request, cat, slug, name, id):
        cat = Categorys.objects.get(slug=slug)
        print(cat.profile_id.id)

        product = Products.objects.get(id=id)
        fotos = FotoProduct.objects.filter(
            product_id=product.id).order_by('id')
        fotos_mix = {}
        i = 0
        for i in range(len(fotos)):
            if fotos[i].another_min == True:
                fotos_mix.update({fotos[i]: fotos[i - 1]})
        ctx = {
            "fotos_mix": fotos_mix,
            "product": product,
            "cat": cat,
        }
        if cat.profile_id.id == 1:
            return TemplateResponse(request, "store_product_gsm_details.html",
                                    ctx)
        if cat.profile_id.id == 2 or cat.profile_id.id == 3:
            return TemplateResponse(request, "store_product_grav_details.html",
                                    ctx)


def error404(request, *args):
    return render(request, '404.html')


def error500(request, *args):
    return render(request, '404.html')