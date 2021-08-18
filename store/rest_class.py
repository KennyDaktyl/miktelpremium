from miktel.models import *
from rest_framework import routers, serializers, viewsets, generics
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse

from store.rest_class import *
import json
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework import mixins, viewsets
from rest_framework import permissions
import json
# import django_filters.rest_framework
from rest_framework import filters
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from django.db.models import Q
from functools import reduce
from operator import or_, and_


# Serializers define the API representation.
class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Czesc
        depth = 3
        fields = '__all__'
        ordering_fields = "__all__"
        ordering = (
            "marka",
            "nazwa",
            "typ",
            'slug',
        )


# Serializers define the API representation.
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Typ
        depth = 1
        fields = ('nazwa', 'typ_slug')
        ordering_fields = "__all__"
        ordering = ("nazwa", )


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefon
        depth = 3
        fields = (
            'id',
            'marka',
            'nazwa',
            'slug',
            'kategoria',
            'magazyn_aktualny',
            'cena_sprzed',
        )
        ordering_fields = "__all__"
        ordering = ("nazwa", )


class ItemsViewSet(viewsets.ModelViewSet):
    # Login authorisiation for client
    # permission_classes = [permissions.DjangoModelPermissions]

    queryset = Czesc.objects.all()
    serializer_class = ItemsSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        if search != None:
            search = search.split(" ")
            search_d = list(search)
            items = Czesc.objects.all().order_by('marka').order_by('nazwa')

            q_filter = reduce(and_, (Q(nazwa__icontains=search)
                                     | Q(marka__nazwa__icontains=search)
                                     | Q(typ__nazwa__icontains=search)
                                     for search in search))
            items = Czesc.objects.filter(q_filter)
            return Czesc.objects.filter(q_filter).order_by('nazwa')[0:20]


class PhoneListView(viewsets.ModelViewSet):
    # Login authorisiation for client
    # permission_classes = [permissions.DjangoModelPermissions]

    queryset = Telefon.objects.filter(dostepny=True)
    serializer_class = PhoneSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        if search != None:
            search = search.split(" ")
            search_d = list(search)
            q_filter = reduce(and_, (Q(nazwa__icontains=search)
                                     | Q(marka__nazwa__icontains=search)
                                     | Q(kategoria__nazwa__icontains=search)
                                     for search in search))

            return Telefon.objects.filter(q_filter).filter(
                dostepny=True).order_by('nazwa')[0:20]


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        depth = 2
        fields = '__all__'
        ordering_fields = "__all__"
        ordering = (
            "name",
            "category_id",
            "slug",
        )


class CategorysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorys
        depth = 2
        fields = '__all__'
        ordering_fields = "__all__"
        ordering = ("name", )


class ProductsGSMApiView(viewsets.ModelViewSet):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        if search != None:
            search = search.split(" ")
            search_d = list(search)

            q_filter = reduce(and_, (Q(name__icontains=search)
                                     | Q(category_id__name__icontains=search)
                                     for search in search))

            return Products.objects.filter(q_filter).filter(
                category_id__profile_id=1).filter(
                    is_active=True).order_by('name')[0:20]


class ProductsGravApiView(viewsets.ModelViewSet):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        if search != None:
            search = search.split(" ")
            search_d = list(search)

            q_filter = reduce(and_, (Q(name__icontains=search)
                                     | Q(category_id__name__icontains=search)
                                     for search in search))

            return Products.objects.filter(q_filter).filter(
                category_id__profile_id__in=[2, 3]).filter(
                    is_active=True).order_by('name')[0:20]


class ProductsStampApiView(viewsets.ModelViewSet):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        if search != None:
            search = search.split(" ")
            search_d = list(search)

            q_filter = reduce(and_, (Q(name__icontains=search)
                                     | Q(category_id__name__icontains=search)
                                     for search in search))

            return Products.objects.filter(q_filter).filter(
                category_id__profile_id=4).filter(
                    is_active=True).order_by('name')[0:20]


class ProductsKeysApiView(viewsets.ModelViewSet):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search')
        if search != None:
            search = search.split(" ")
            search_d = list(search)

            q_filter = reduce(and_, (Q(name__icontains=search)
                                     | Q(category_id__name__icontains=search)
                                     for search in search))

            return Products.objects.filter(q_filter).filter(
                category_id__profile_id=5).filter(
                    is_active=True).order_by('name')[0:20]


router = routers.DefaultRouter()
router.register(r"items", ItemsViewSet, basename="items_api_view"),
router.register(r"phones", PhoneListView, basename="phones_api_view"),
router.register(r"products/gsm",
                ProductsGSMApiView,
                basename="products_gsm_api_view"),
router.register(r"products/grav",
                ProductsGravApiView,
                basename="products_grav_api_view"),
router.register(r"products/stamp",
                ProductsStampApiView,
                basename="products_stamp_api_view"),
router.register(r"products/keys",
                ProductsKeysApiView,
                basename="products_keys_api_view"),
