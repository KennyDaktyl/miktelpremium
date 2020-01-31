from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin

# Generici i szablony
from django.views import View
from django.views.generic.edit \
    import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from weasyprint import HTML

from django.db.models import Q
from django.db.models import Count

from googlevoice import Voice
from googlevoice.util import input
# from smsapi.client import SmsApiPlClient

from django.core.paginator import Paginator

from miktel.models import *
from miktel.forms import *
from miktel.function import *
# from miktel.hasla import *

rok = datetime.now().year
miesiac = datetime.now().month
page_records=40

# Create your views here.


class MainView(View):
    def get(self, request):
        sklep=Sklep.objects.filter(serwis_zew=False)
        # telefon=Telefon.objects.filter(sklep=1).count()
        # print(telefon)
        ctx={'sklep':sklep}
        return TemplateResponse(request, "klient.html", ctx)


class UserLoginView(View):
    def get(self, request):
        form = LoginForm()
        # send(50602998, 'Zalogowano')
        return render(request, "user_login.html", context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username, password = form.cleaned_data.values()
            user = authenticate(username=username, password=password)
            # user = MyUser.objects.get(username=username, password=password)
            if user is not None:
                login(request, user)
                id_user=request.user.id
                url="/profil/{}".format(id_user)
                return redirect(url)
            else:
                return HttpResponse('Użytkownik {username} niepoprawny')
        return render(request, "/user_login.html", context={'form': form})


@login_required
def User_Logout(request):
    logout(request)

    return redirect('/')

@method_decorator(login_required, name='dispatch')
class ProfilView(PermissionRequiredMixin,View):
    permission_required='miktel.view_myuser'
    def get(self, request, pk):
        page_records=40
        pracownik = request.user
        sklepy = pracownik.sklep.all()
        form=PageRecordsForm()
        # global page_records
        # page_records=40
        ilosc_wynikow= page_records
        print(ilosc_wynikow)
        # print(sklepy)
        ctx = {'form':form,'sklepy': sklepy,'pracownik':pracownik,'ilosc':ilosc_wynikow}
        return TemplateResponse(request, "profil_user.html", ctx)

    def post(self, request, pk):
        pracownik = request.user
        sklepy = pracownik.sklep.all()

        form=PageRecordsForm(request.POST)
        if form.is_valid():
            global page_records
            page_records = int(form.cleaned_data['page_records'])
            
            ctx = {'sklepy': sklepy,'pracownik':pracownik,'ilosc':page_records}
            url="/profil/{}".format(pracownik.id)
            
            sklep_sesja = request.POST.get('sklep_sesja')
            if sklep_sesja != "" and sklep_sesja is not None:
                sklep_instancja = Sklep.objects.get(pk=sklep_sesja)
                user = MyUser.objects.get(pk=pracownik.id)
                user = MyUser.objects.get(pk=pracownik.id)
                user.sklep_dzisiaj = sklep_instancja
                user.save()
                
                request.user.sklep_dzisiaj = sklep_instancja
                print("jestem, tutaj")
                return redirect(url, ctx)
            
            ctx = {'sklepy': sklepy,'pracownik':pracownik, 'ilosc':page_records,'form':form}
            return TemplateResponse(request, "profil_user.html", ctx)


        else:
            ilosc_rekordow = request.POST.get('page_records')
            sklep_sesja = request.POST.get('sklep_sesja')
            if sklep_sesja != "":
                print("ustawiam sklep")
                ilosc=request.POST.get('ilosc')
                sklep_instancja = Sklep.objects.get(pk=sklep_sesja)
                user = MyUser.objects.get(pk=pracownik.id)
                user.sklep_dzisiaj = sklep_instancja
                user.save()
                
                request.user.sklep_dzisiaj = sklep_instancja
                # global page_records
               
                page_records=40
                form=PageRecordsForm()

                ctx = {'sklepy': sklepy,'pracownik':pracownik, 'ilosc':page_records,'form':form}
                return TemplateResponse(request, "profil_user.html", ctx)

@method_decorator(login_required, name='dispatch')
class PageRecordsView(PermissionRequiredMixin,View):
    permission_required='miktel.view_myuser'
    def post(self, request):
        pracownik = request.user
        sklepy = pracownik.sklep.all()
        
        form=PageRecordsForm(request.POST)
        if form.is_valid():
            global page_records
            page_records = int(form.cleaned_data['page_records'])
            
            ctx = {'sklepy': sklepy,'pracownik':pracownik,'ilosc':page_records}
            url="/profil/{}".format(pracownik.id)
            return redirect(url, ctx)
        else:
            print('Nie jest valid')
            return TemplateResponse(request,'form_errors.html')

@method_decorator(login_required, name='dispatch')
class DodajMyUserView(PermissionRequiredMixin,CreateView):
    permission_required='miktel.add_myuser'
    model = MyUser
    fields = '__all__'
    success_url = reverse_lazy("widok_klienta")

@method_decorator(login_required, name='dispatch')
class DodajPracownikaView(PermissionRequiredMixin,CreateView):
    permission_required = 'miktel.add_myuser'
    raise_exception = True
    permission_denied_message = 'Brak dostępu do tego widoku'
    model = MyUser
    fields = '__all__'
    success_url = reverse_lazy("widok_klienta")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ListaMyUserView(PermissionRequiredMixin,View):
    permission_required='miktel.view_myuser'
    def get(self, request):
        pracownicy = MyUser.objects.all().order_by('last_name')
        ctx = {'pracownicy': pracownicy}
        return render(request, 'lista_pracownikow.html', ctx)

@method_decorator(login_required, name='dispatch')
class EdycjaMyUserView(PermissionRequiredMixin,UpdateView):
    permission_required='miktel.change_myuser'
    model = MyUser
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/lista_uzytkownikow/')


@method_decorator(login_required, name='dispatch')
class UstawFotoProfilView(PermissionRequiredMixin,View):
    permission_required='miktel.view_myuser'
    def get(self, request, pk):
        form=UstawFotoForm()
        ctx = {'form':form}
        return TemplateResponse(request, "ustaw_foto.html", ctx)
        # return TemplateResponse(request, "ustaw_foto.html", )
    def post(self, request, pk):
        pracownik = request.user
        sklepy = pracownik.sklep.all()
        form=UstawFotoForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.cleaned_data['foto']
            title = form.cleaned_data['title']
            alt = form.cleaned_data['alt']
            foto=Foto.objects.create(foto=foto,title=title,alt=alt)

            pracownik.foto=foto
            pracownik.save()

            url="/profil/{}".format(pracownik.id)
            return redirect(url)
        else:
            print('Nie jest valid')
            return TemplateResponse(request,'form_errors.html')

@method_decorator(login_required, name='dispatch')
class UstawHasloView(PermissionRequiredMixin,View):
    permission_required='miktel.view_myuser'
    def get(self, request, pk):
        form=UstawHasloForm()
        ctx = {'form':form}
        return TemplateResponse(request, "ustaw_haslo.html", ctx)
    def post(self, request, pk):
        pracownik = request.user
        sklepy = pracownik.sklep.all()
        form=UstawHasloForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            print(password)
            pracownik.set_password(password)
            print(pracownik.password)
            pracownik.save()

            # def form_valid(self, form):
            #     user = form.save(commit=False)
            #     user.set_password(user.password)
            #     return super().form_valid(form)

            url="/profil/{}".format(pracownik.id)
            return redirect(url)
        else:
            print('Nie jest valid')
            return TemplateResponse(request,'form_errors.html')

#SEKCJA TELEFON
@method_decorator(login_required, name='dispatch')
class TelefonCreateView(PermissionRequiredMixin,View):
    permission_required = 'miktel.add_telefon'
    def get(self, request):
        form = TelefonCreateForm
        ctx = {'form': form}
        return render(request, 'phone_create.html', ctx)

    def post(self, request):
        form = TelefonCreateForm(request.POST)
        if form.is_valid():
            stan = form.cleaned_data['stan']
            kategoria = form.cleaned_data['kategoria']
            marka = form.cleaned_data['marka']
            nazwa = form.cleaned_data['nazwa']
            imei = form.cleaned_data['imei']
            cena_zak = form.cleaned_data['cena_zak']
            cena_sprzed = form.cleaned_data['cena_sprzed']

            pracownik = request.user
            shop_buying = pracownik.sklep_dzisiaj

            Telefon.objects.create(marka=marka,
                                    stan=stan,
                                   nazwa=nazwa,
                                   sklep=shop_buying,
                                   imei=imei,
                                   kategoria=kategoria,
                                   cena_zak=cena_zak,
                                   cena_sprzed=cena_sprzed,
                                   pracownik_zak=pracownik,
                                   data_wprow=datetime.now(),
                                   magazyn_aktualny=shop_buying)

            return HttpResponseRedirect('/telefony_magazyn/')
        else:
            print('Nie jest valid')
            return HttpResponseRedirect('/')

@method_decorator(login_required, name='dispatch')
class TelefonyMagazynView(PermissionRequiredMixin,View):
    permission_required = 'miktel.view_telefon'
    def get(self, request):
        telefony = Telefon.objects.filter(dostepny=True).filter(zawieszony=False).order_by(
            'marka', 'nazwa', 'cena_sprzed')
        faktury = FakturaZakupu.objects.filter(telefon__in=telefony)
        umowy = UmowaKomisowaNew.objects.filter(phones__in=telefony)
        global page_records
        page = request.GET.get('page')
        paginator = Paginator(telefony, page_records)
        telefony_pagi = paginator.get_page(page)
        shops=Sklep.objects.filter(serwis_zew=False)

        ctx = {
            'shops':shops,
            'telefony': telefony_pagi,
            'faktury': faktury,
            'umowy': umowy,
            'paginator': paginator,
            'page_records':page_records
        }
        return TemplateResponse(request, "telefony_magazyn.html", ctx)
    def post(self, request):
        szukaj = request.POST.get('szukaj')

        telefony = Telefon.objects.filter(dostepny=True)
        telefony = telefony.filter(
            Q(marka__nazwa__icontains=szukaj) | Q(nazwa__icontains=szukaj)
            | Q(kategoria__nazwa__icontains=szukaj)
            | Q(imei__icontains=szukaj))

        faktury = FakturaZakupu.objects.filter(telefon__in=telefony)
        umowy = UmowaKomisowaNew.objects.filter(phones__in=telefony)
        # print(faktury)
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(telefony, page_records)
        telefony_pagi = paginator.get_page(page)
        shops=Sklep.objects.filter(serwis_zew=False)

        ctx = {
            'shops':shops,
            'telefony': telefony_pagi,
            'faktury': faktury,
            'umowy': umowy,
            'page_records':page_records
            
        }
        return TemplateResponse(request, "telefony_magazyn.html", ctx)

@method_decorator(login_required, name='dispatch')
class TelefonyMagazynFilterView(PermissionRequiredMixin,View):
    permission_required = 'miktel.view_telefon'
    def get(self, request,pk):
        telefony = Telefon.objects.filter(magazyn_aktualny=pk).filter(dostepny=True).filter(zawieszony=False).order_by(
            'marka', 'nazwa', 'cena_sprzed')
        faktury = FakturaZakupu.objects.filter(telefon__in=telefony)
        umowy = UmowaKomisowaNew.objects.filter(phones__in=telefony)
        global page_records
        page = request.GET.get('page')
        paginator = Paginator(telefony, page_records)
        telefony_pagi = paginator.get_page(page)
        shops=Sklep.objects.filter(serwis_zew=False)

        ctx = {
            'shops':shops,
            'telefony': telefony_pagi,
            'faktury': faktury,
            'umowy': umowy,
            'paginator': paginator,
            'page_records':page_records
        }
        return TemplateResponse(request, "telefony_magazyn.html", ctx)
    def post(self, request,pk):
        szukaj = request.POST.get('szukaj')

        telefony = Telefon.objects.filter(magazyn_aktualny=pk).filter(dostepny=True).filter(zawieszony=False).order_by(
            'marka', 'nazwa', 'cena_sprzed')
        telefony = telefony.filter(
            Q(marka__nazwa__icontains=szukaj) | Q(nazwa__icontains=szukaj)
            | Q(kategoria__nazwa__icontains=szukaj)
            | Q(imei__icontains=szukaj))

        faktury = FakturaZakupu.objects.filter(telefon__in=telefony)
        umowy = UmowaKomisowaNew.objects.filter(phones__in=telefony)
        # print(faktury)
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(telefony, page_records)
        telefony_pagi = paginator.get_page(page)
        shops=Sklep.objects.filter(serwis_zew=False)

        ctx = {
            'shops':shops,
            'telefony': telefony_pagi,
            'faktury': faktury,
            'umowy': umowy,
            'page_records':page_records
            
        }
        return TemplateResponse(request, "telefony_magazyn.html", ctx)

@method_decorator(login_required, name='dispatch')
class TelefonyZawieszoneView(PermissionRequiredMixin,View):
    permission_required = 'miktel.view_telefon'
    def get(self, request):
        telefony = Telefon.objects.filter(zawieszony=True).order_by(
            'marka', 'nazwa', 'cena_sprzed')
        faktury = FakturaZakupu.objects.filter(telefon__in=telefony)
        umowy = UmowaKomisowaNew.objects.filter(phones__in=telefony)
        global page_records
        page = request.GET.get('page')
        paginator = Paginator(telefony, page_records)
        telefony_pagi = paginator.get_page(page)
        shops=Sklep.objects.filter(serwis_zew=False)

        ctx = {
            'shops':shops,
            'telefony': telefony_pagi,
            'faktury': faktury,
            'umowy': umowy,
            'paginator': paginator,
            'page_records':page_records
        }
        return TemplateResponse(request, "telefony_zawieszone.html", ctx)

    def post(self, request):
        szukaj = request.POST.get('szukaj')

        telefony = Telefon.objects.filter(zawieszony=True)
        telefony = telefony.filter(
            Q(marka__nazwa__icontains=szukaj) | Q(nazwa__icontains=szukaj)
            | Q(kategoria__nazwa__icontains=szukaj)
            | Q(imei__icontains=szukaj))

        faktury = FakturaZakupu.objects.filter(telefon__in=telefony)
        umowy = UmowaKomisowaNew.objects.filter(phones__in=telefony)
        # print(faktury)
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(telefony, page_records)
        telefony_pagi = paginator.get_page(page)
        shops=Sklep.objects.filter(serwis_zew=False)

        ctx = {
            'shops':shops,
            'telefony': telefony_pagi,
            'faktury': faktury,
            'umowy': umowy,
            'page_records':page_records
            
        }
        return TemplateResponse(request, "telefony_magazyn.html", ctx)

@method_decorator(login_required, name='dispatch')
class TelefonyReklamacjaView(PermissionRequiredMixin,UpdateView):
    permission_required = 'miktel.change_telefon'
    model = Telefon
    fields = ['info','zawieszony','data_zmiany']
    template_name_suffix = ('_update_form')
    success_url = ('/telefony_zawieszone/')  

@method_decorator(login_required, name='dispatch')
class TelefonyMagazynChangeView(PermissionRequiredMixin,UpdateView):
    permission_required = 'miktel.change_telefon'
    model = Telefon
    fields = ['magazyn_aktualny']
    template_name_suffix = ('_update_form')
    success_url = ('/telefony_magazyn/')  

@method_decorator(login_required, name='dispatch')
class TelefonyMagazynInfoView(PermissionRequiredMixin,UpdateView):
    permission_required = 'miktel.change_telefon'
    model = Telefon
    fields = ['info','zawieszony']
    template_name_suffix = ('_update_form')
    success_url = ('/telefony_magazyn/')


@method_decorator(login_required, name='dispatch')
class TelefonySprzedaneView(PermissionRequiredMixin,View):
    permission_required = 'miktel.view_telefon'
    def get(self, request):
        telefony = Telefon.objects.filter(dostepny=False).order_by('-data_sprzed',
            'marka', 'nazwa', 'cena_sprzed')
        faktury = FakturaZakupu.objects.filter(telefon__in=telefony)
        umowy = UmowaKomisowaNew.objects.filter(phones__in=telefony)
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(telefony, page_records)
        telefony_pagi = paginator.get_page(page)
        shops=Sklep.objects.filter(serwis_zew=False)

        ctx = {'shops':shops,'telefony': telefony_pagi, 'faktury': faktury, 'umowy': umowy,'page_records':page_records}
        return TemplateResponse(request, "telefony_sprzedane.html", ctx)

    def post(self, request):
        szukaj = request.POST.get('szukaj')

        Telefony_dostepne = Telefon.objects.filter(dostepny=False).order_by('-data_sprzed',
            'marka', 'nazwa', 'cena_sprzed')
        telefony = Telefony_dostepne.filter(
            Q(marka__nazwa__icontains=szukaj) | Q(nazwa__icontains=szukaj)
            | Q(kategoria__nazwa__icontains=szukaj)
            | Q(imei__icontains=szukaj))
        faktury = FakturaZakupu.objects.filter(telefon__in=telefony)
        umowy = UmowaKomisowaNew.objects.filter(phones__in=telefony)
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(telefony, page_records)
        telefony_pagi = paginator.get_page(page)
        shops=Sklep.objects.filter(serwis_zew=False)

        ctx = {'shops':shops,'telefony': telefony_pagi, 'faktury': faktury, 'umowy': umowy,'page_records':page_records}
        return TemplateResponse(request, "telefony_sprzedane.html", ctx)

@method_decorator(login_required, name='dispatch')
class TelefonySprzedaneMagazynFilterView(PermissionRequiredMixin,View):
    permission_required = 'miktel.view_telefon'
    def get(self, request,pk):
        telefony = Telefon.objects.filter(magazyn_aktualny=pk).filter(dostepny=False).order_by('-data_sprzed',
            'marka', 'nazwa', 'cena_sprzed')
        faktury = FakturaZakupu.objects.filter(telefon__in=telefony)
        umowy = UmowaKomisowaNew.objects.filter(phones__in=telefony)
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(telefony, page_records)
        telefony_pagi = paginator.get_page(page)
        shops=Sklep.objects.filter(serwis_zew=False)

        ctx = {'shops':shops,'telefony': telefony_pagi, 'faktury': faktury, 'umowy': umowy,'page_records':page_records}
        return TemplateResponse(request, "telefony_sprzedane.html", ctx)

    def post(self, request,pk):
        szukaj = request.POST.get('szukaj')

        Telefony_dostepne = Telefon.objects.filter(magazyn_aktualny=pk).filter(dostepny=False).order_by('-data_sprzed',
            'marka', 'nazwa', 'cena_sprzed')
        telefony = Telefony_dostepne.filter(
            Q(marka__nazwa__icontains=szukaj) | Q(nazwa__icontains=szukaj)
            | Q(kategoria__nazwa__icontains=szukaj)
            | Q(imei__icontains=szukaj))
        faktury = FakturaZakupu.objects.filter(telefon__in=telefony)
        umowy = UmowaKomisowaNew.objects.filter(phones__in=telefony)
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(telefony, page_records)
        telefony_pagi = paginator.get_page(page)
        shops=Sklep.objects.filter(serwis_zew=False)

        ctx = {'shops':shops,'telefony': telefony_pagi, 'faktury': faktury, 'umowy': umowy,'page_records':page_records}
        return TemplateResponse(request, "telefony_sprzedane.html", ctx)


@method_decorator(login_required, name='dispatch')
class SellPhonesView(PermissionRequiredMixin,View):
    permission_required = 'miktel.view_telefon'
    def get(self, request, pk):
        telefon = Telefon.objects.get(pk=pk)
        faktura = FakturaZakupu.objects.all()
        umowa = UmowaKomisowaNew.objects.filter(phones=pk)
        
        numer_faktury = "Brak dokumentu zakupu"
        if len(umowa) == 0:
            for el in faktura:
                if telefon in el.telefon.all():
                    numer_faktury = el.numer
        if len(umowa) == 1:
            for el in umowa:
                numer_faktury = el.number

        ctx = {'telefon': telefon, "numer_faktury": numer_faktury}
        return TemplateResponse(request, "selling_phones.html", ctx)

    def post(self, request, pk):
        tel_id = request.POST.get('tel_id')
        cena_sprz = request.POST.get('cena_sprz')
        print(request.user.id)

        telefon = Telefon.objects.get(pk=int(tel_id))
        telefon.cena_sprzed = cena_sprz
        telefon.dostepny = False
        telefon.pracownik_sprzed = request.user
        telefon.sklep_sprzed = request.user.sklep_dzisiaj
        telefon.data_sprzed=datetime.now()
        telefon.save()

        usluga_inst = Usluga.objects.get(sprzedaz=True)
        model = str(telefon.marka) + " " + (telefon.nazwa)

        premia = PremiaJob.objects.filter(usluga=usluga_inst).last()

        if not premia:
            print("jestem Tuataj not premia")
            PremiaJob.objects.create(check=telefon.id,
                                     sklep=request.user.sklep_dzisiaj,
                                     pracownik=request.user,
                                     usluga=usluga_inst,
                                     model=model,
                                     cena_klient=cena_sprz,
                                     koszt=telefon.cena_zak)

            return HttpResponseRedirect('/telefony_sprzedane/')

        else:
            if premia.check != telefon.id:
                print(premia.check)
                print(telefon.id)
                PremiaJob.objects.create(check=telefon.id,
                                         sklep=request.user.sklep_dzisiaj,
                                         pracownik=request.user,
                                         usluga=usluga_inst,
                                         model=model,
                                         cena_klient=cena_sprz,
                                         koszt=telefon.cena_zak)

                subject = "Sprzedano telefon w {} przez {}".format(
                    telefon.sklep_sprzed, telefon.pracownik_sprzed)
                text = "{} sprzedał {} {} za {}".format(
                    request.user,
                    telefon.marka,
                    telefon.nazwa,
                    telefon.cena_sprzed,
                )
                # send_email(subject, text)
                return HttpResponseRedirect('/telefony_sprzedane/')
            else:
                return HttpResponseRedirect('/telefony_sprzedane/')

@method_decorator(login_required, name='dispatch')
class WystawTelefonView(PermissionRequiredMixin,UpdateView):
    permission_required = 'miktel.change_telefon'
    model = Telefon
    fields = ['kategoria', 'stan', 'cena_sprzed', 'zdjecia']
    template_name_suffix = ('_update_form')
    success_url = ('/')


@method_decorator(login_required, name='dispatch')
class SzczegolyTelefonuView(PermissionRequiredMixin,UpdateView):
    permission_required = 'miktel.change_telefon'
    model = Telefon
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/')




#SEKCJA UMOWA KOMISOWA
@method_decorator(login_required, name='dispatch')
class UmowaKomisowaView(PermissionRequiredMixin,View):
    permission_required = 'miktel.add_umowakomisowanew'
    def get(self, request):
        form = UmowaKomisowaForm()
        return render(request, 'invoice_form.html', {'form': form})

    def post(self, request):
        form = UmowaKomisowaForm(request.POST)
        if form.is_valid():
            phones = form.cleaned_data['phones']
            komitent = form.cleaned_data['komitent']
            adres_komitenta = form.cleaned_data['adres_komitenta']
            numer_dowodu = form.cleaned_data['numer_dowodu']

            pracownik = request.user
            sklep_sesja = pracownik.sklep_dzisiaj.id
            sklep_instancja = Sklep.objects.get(pk=sklep_sesja)
            pracownik_instancja = MyUser.objects.get(pk=pracownik.id)

            number = numer_umowy()
            umowa = UmowaKomisowaNew.objects.create(
                number=number,
                sklep_zak=sklep_instancja,
                pracownik_zak=pracownik_instancja,
                komitent=komitent,
                adres_komitenta=adres_komitenta,
                numer_dowodu=numer_dowodu,
                phones=phones)
            telefon_instancja = Telefon.objects.get(pk=phones.id)
            telefon_instancja.dokument = True
            telefon_instancja.nr_doc = number 
            telefon_instancja.save()
            return HttpResponseRedirect('/checking_document/')
        else:
            print('Nie jest valid')
            return HttpResponseRedirect('/checking_document/')

@method_decorator(login_required, name='dispatch')
class ListaUmowView(PermissionRequiredMixin,View):
    permission_required = 'miktel.view_umowakomisowanew'
    def get(self, request):
        umowy = UmowaKomisowaNew.objects.all().order_by('-id')
        telefon = Telefon.objects.all().last()

        page = request.GET.get('page')
        global page_records
        paginator = Paginator(umowy, page_records)
        umowy_pagi = paginator.get_page(page)
        ctx = {'umowy': umowy_pagi,'page_records':page_records}
        return render(request, 'lista_umow.html', ctx)

    def post(self, request):
        szukaj = request.POST.get('szukaj')

        umowa = UmowaKomisowaNew.objects.filter(
            Q(number__icontains=szukaj) | Q(komitent__icontains=szukaj)
            | Q(phones__nazwa__icontains=szukaj)
            | Q(phones__marka__nazwa__icontains=szukaj)
            | Q(phones__imei__icontains=szukaj))

        ctx = {'umowy': umowa,'page_records':page_records}
        return TemplateResponse(request, "lista_umow.html", ctx)

@method_decorator(login_required, name='dispatch')
class CheckingDocumentView(PermissionRequiredMixin,View):
    permission_required = 'miktel.add_umowakomisowanew'
    def get(self, request):
        pracownik = request.user
        sklepy = pracownik.sklep.all()
        umowa = UmowaKomisowaNew.objects.last()

        usluga = Usluga.objects.get(zakup=True)

        return render(request, 'checking_document.html', {
            'umowa': umowa,
            'sklepy': sklepy
        })

    def post(self, request):
        tele_id = request.POST.get('tele_id')
        sklep_dzisiaj = request.user.sklep_dzisiaj
        umowa = UmowaKomisowaNew.objects.last()
        umowa.sklep_zak = sklep_dzisiaj
        umowa.save()
        pracownik = request.user
        sklepy = pracownik.sklep.all()
        umowa = UmowaKomisowaNew.objects.last()

        usluga = Usluga.objects.get(zakup=True)
        premia = PremiaJob.objects.filter(usluga=usluga).last()

        usluga = Usluga.objects.get(zakup=True)
        model = str(umowa.phones.marka) + " " + str(
            umowa.phones.nazwa) + " " + str(umowa.phones.cena_zak)

        if not premia:
            PremiaJob.objects.create(check=tele_id,
                                     sklep=request.user.sklep_dzisiaj,
                                     pracownik=request.user,
                                     usluga=usluga,
                                     model=model)
            subject = "Zakupiono telefon na Umowe w {} przez {}".format(
                    umowa.request.user.sklep_dzisiaj, umowa.pracownik_zak)
            text = "{} kupil {} {} za {} ".format(umowa.pracownik_zak,
                                                      umowa.phones.marka,
                                                      umowa.phones.nazwa,
                                                      umowa.phones.cena_zak)
            send_email(subject, text)
            return HttpResponseRedirect('/lista_umow/')

            
        else:
            if int(premia.check) != int(tele_id):
               
                PremiaJob.objects.create(check=tele_id,
                                         sklep=request.user.sklep_dzisiaj,
                                         pracownik=request.user,
                                         usluga=usluga,
                                         model=model)

                subject = "Zakupiono telefon na Umowe w {} przez {}".format(
                    umowa.sklep_zak, umowa.pracownik_zak)
                text = "{} kupil {} {} za {} ".format(umowa.pracownik_zak,
                                                      umowa.phones.marka,
                                                      umowa.phones.nazwa,
                                                      umowa.phones.cena_zak)
                send_email(subject, text)
                return HttpResponseRedirect('/lista_umow/')
            else:
                return HttpResponseRedirect('/lista_umow/')

@method_decorator(login_required, name='dispatch')
class EdycjaUmowyView(PermissionRequiredMixin,UpdateView):
    permission_required = 'miktel.change_umowakomisowanew'
    model = UmowaKomisowaNew
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/lista_umow/')

@method_decorator(login_required, name='dispatch')
class UmowaIdView(PermissionRequiredMixin,View):
    permission_required = 'miktel.change_umowakomisowanew'
    model = UmowaKomisowaNew
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/lista_umow/')

@method_decorator(login_required, name='dispatch')
class DeleteDocumentView(PermissionRequiredMixin,View):
    permission_required='miktel.delete_umowakomisowanew'
    def get(self, request, pk):
        umowa = UmowaKomisowaNew.objects.get(pk=pk)
        phones = Telefon.objects.get(pk=umowa.phones.id)
        phones.dokument = False
        phones.save()
        umowa.delete()

        return redirect('umowa_komisowa')

@method_decorator(login_required, name='dispatch')
class DeleteFakturaZakupuView(PermissionRequiredMixin,View):
    permission_required='miktel.delete_fakturazakupu'
    def get(self, request, pk):
        faktura = FakturaZakupu.objects.get(pk=pk)
        phones = Telefon.objects.filter(nr_doc=faktura.numer)
        for el in phones:
            el.dokument = False
            el.nr_doc=""
            el.save()
        faktura.delete()

        return redirect('telefony_magazyn')


#SEKCJA FAKTURA ZAKUPU
@method_decorator(login_required, name='dispatch')
class FakturaZakupuView(PermissionRequiredMixin,View):
    permission_required='miktel.add_fakturazakupu'
    def get(self, request):
        form = FakturaZakupuForm()
        return render(request, 'invoice_form.html', {'form': form})

    def post(self, request):
        form = FakturaZakupuForm(request.POST)
        if form.is_valid():
            telefon = form.cleaned_data['telefon']
            numer = form.cleaned_data['numer']
            hurtownia = form.cleaned_data['hurtownia']

            pracownik = request.user
            sklep_sesja = pracownik.sklep_dzisiaj
            sklep_instancja = Sklep.objects.get(pk=sklep_sesja.id)
            hurtownia_instancja = Hurtownia.objects.get(nazwa=hurtownia)
            pracownik_instancja = MyUser.objects.get(pk=pracownik.id)
            telefony_instancja = []

            faktura = FakturaZakupu.objects.create(numer=numer,
                                                   sklep=sklep_instancja,
                                                   hurtownia=hurtownia,
                                                   pracownik_zak=pracownik)
            for el in telefon:
                faktura.telefon.add(el)
                telefon = Telefon.objects.get(pk=el.id)
                telefon.dokument = True
                telefon.dostepny = True
                telefon.nr_doc=numer
                telefon.save()
                faktura.save()

            return HttpResponseRedirect('/checking_invoice/')
        else:
            print('Nie jest valid')
            return HttpResponseRedirect('/lista_faktur/')


@method_decorator(login_required, name='dispatch')
class CheckingInvoiceView(PermissionRequiredMixin,View):
    permission_required='miktel.add_fakturazakupu'
    def get(self, request):
        pracownik = request.user
        sklepy = pracownik.sklep.all()
        faktura = FakturaZakupu.objects.last()
        tel_lista = ','.join(el.nazwa for el in faktura.telefon.all())
        # if len(faktura.telefon.all()) > 1:
        total_price = []
        lista = faktura.telefon.all()
        for tel in lista:
            total_price.append(tel.cena_zak)
        # else:
        # total_price = faktura.telefon.cena_zak
        total = sum(total_price)
        total_minus_tax = round(total / 1.23, 2)

        subject = "Pracownik {} wprowadzil fakture nr {} w {} zawierajaca {}".format(
            pracownik, faktura.numer, faktura.sklep, tel_lista,
            pracownik.sklep_dzisiaj)
        text = "Wprowadzono fakture w {}".format(pracownik.sklep_dzisiaj)
        # send_email(subject, text)
        return render(request, 'checking_invoice.html', {
            'faktura': faktura,
            'total': total,
            'total_minus_tax': total_minus_tax
        })

    def post(self, request):
        sklep_sesja = request.POST.get('sklep_sesja')
        if sklep_sesja != "":
            sklep_dzisiaj = Sklep.objects.get(pk=sklep_sesja)
            umowa = UmowaKomisowaNew.objects.last()
            umowa.sklep_zak = sklep_dzisiaj
            umowa.save()
            pracownik = request.user
            sklepy = pracownik.sklep.all()
            umowa = UmowaKomisowaNew.objects.last()

            return render(request, 'checking_document.html', {
                'umowa': umowa,
                'sklepy': sklepy
            })
        else:
            return redirect('/checking_document/')


@method_decorator(login_required, name='dispatch')
class FakturaIdView(PermissionRequiredMixin,View):
    permission_required='miktel.add_fakturazakupu'
    def get(self, request, pk):
        umowa = FakturaZakupu.objects.get(telefon=pk)
        ctx = {'umowa': umowa}
        return render(request, 'faktura_id.html', ctx)


@method_decorator(login_required, name='dispatch')
class ListaFakturView(PermissionRequiredMixin,View):
    permission_required='miktel.view_fakturazakupu'
    def get(self, request):
        faktury = FakturaZakupu.objects.all().order_by('-id')
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(faktury, page_records)
        faktury_pagi = paginator.get_page(page)
        
        ctx = {'faktury': faktury_pagi}
        return render(request, 'lista_faktur.html', ctx)

    def post(self, request):
        szukaj = request.POST.get('szukaj')

        faktury = FakturaZakupu.objects.filter(
            Q(numer__icontains=szukaj) | Q(hurtownia__nazwa__icontains=szukaj)
            | Q(telefon__imei__icontains=szukaj)
            | Q(telefon__nazwa__icontains=szukaj)
            | Q(telefon__marka__nazwa__icontains=szukaj))
        
        ctx = {'faktury': faktury}
        return render(request, 'lista_faktur.html', ctx)


@method_decorator(login_required, name='dispatch')
class EdycjaFakturyView(PermissionRequiredMixin,UpdateView):
    permission_required='miktel.change_fakturazakupu'
    model = FakturaZakupu
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/lista_faktur/')

@method_decorator(login_required, name='dispatch')
class DeleteFakturaZakupuView(PermissionRequiredMixin,View):
    permission_required='miktel.delete_fakturazakupu'
    def get(self, request, pk):
        faktura = FakturaZakupu.objects.get(pk=pk)
        phones = Telefon.objects.filter(nr_doc=faktura.numer)
        for el in phones:
            el.dokument = False
            el.nr_doc=""
            el.save()
        faktura.delete()

        return redirect('telefony_magazyn')




#SEKCJA GENEROWANIA PDF
@method_decorator(login_required, name='dispatch')
class GenerujPdfView(View):
    def get(self, request, pk, *args, **kwargs):
        pk = pk
        umowa = UmowaKomisowaNew.objects.get(pk=pk)
        context = {
            'umowa': umowa,
        }
        html_string = render_to_string('umowa_pdf.html', context)

        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/umowapdf.pdf')

        fs = FileSystemStorage('/tmp')
        with fs.open('umowapdf.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response[
                'Content-Disposition'] = 'attachment; filename="umowa_pdf.pdf"'
        return response

@method_decorator(login_required, name='dispatch')
class DodajPDFSerwisView(View):
    def get(self, request, pk, *args, **kwargs):
        pk = pk
        serwis = DodajSerwis.objects.get(pk=pk)
        context = {
            'serwis': serwis,
        }
        html_string = render_to_string('serwis_pdf.html', context)

        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/serwispdf.pdf')

        fs = FileSystemStorage('/tmp')
        with fs.open('serwispdf.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response[
                'Content-Disposition'] = 'attachment; filename="serwis_pdf.pdf"'
        return response



#SEKCJA SERWISY GSM
@method_decorator(login_required, name='dispatch')
class DodajSerwisView(PermissionRequiredMixin,View):
    permission_required='miktel.add_dodajserwis'
    def get(self, request):
        form = GetServiceForm

        ctx = {'form': form}
        return render(request, 'miktel/dodajserwis_form.html', ctx)

    def post(self, request):
        form = GetServiceForm(request.POST)
        if form.is_valid():
            usluga = form.cleaned_data['usluga']
            marka = form.cleaned_data['marka']
            model = form.cleaned_data['model']
            imei = form.cleaned_data['imei']
            cena_zgoda = form.cleaned_data['cena_zgoda']
            numer_telefonu = form.cleaned_data['numer_telefonu']
            imie_nazwisko = form.cleaned_data['imie_nazwisko']
            info = form.cleaned_data['info']

            # usluga_inst = Usluga.objects.get(pk=usluga)

            pracownik = request.user

            DodajSerwis.objects.create(pracownik=pracownik,
                                       sklep=pracownik.sklep_dzisiaj,
                                       marka=marka,
                                       usluga=usluga,
                                       model=model,
                                       imei=imei,
                                       cena_zgoda=cena_zgoda,
                                       numer_telefonu=numer_telefonu,
                                       imie_nazwisko=imie_nazwisko,info=info)

            return HttpResponseRedirect('/lista_serwisow/')
        else:
            print('Nie jest valid')
            return HttpResponseRedirect('/')




@method_decorator(login_required, name='dispatch')
class ListaSerwisowMagazynView(PermissionRequiredMixin,View):
    permission_required='miktel.view_dodajserwis'
    def get(self, request):
        lokal=request.user.sklep_dzisiaj.id
        serwisy = DodajSerwis.objects.filter(naprawa=True).filter(sklep=lokal).order_by('-id')
        # serwisy = DodajSerwis.objects.all().order_by('-id')
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(serwisy, page_records)
        serwisy_pagi = paginator.get_page(page)
        lokal=request.user.sklep_dzisiaj.id
        lokale=Sklep.objects.all()
        
        ctx = {'serwisy': serwisy_pagi,'lokal':lokal,'lokale':lokale}
        return render(request, 'serwisy.html', ctx)
    
    def post(self, request):
        szukaj = request.POST.get('szukaj')

        serwisy_dostepne = DodajSerwis.objects.filter(archiwum=False)
        serwisy = serwisy_dostepne.filter(Q(id__icontains=szukaj) |
            Q(marka__nazwa__icontains=szukaj) | Q(model__icontains=szukaj)
            | Q(imei__icontains=szukaj))
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(serwisy, page_records)
        serwisy_pagi = paginator.get_page(page)
        ctx = {'serwisy': serwisy_pagi}
        return render(request, 'serwisy.html', ctx)

@method_decorator(login_required, name='dispatch')
class ListaSerwisowFilterMagazynView(PermissionRequiredMixin,View):
    permission_required='miktel.view_dodajserwis'
    def get(self, request,pk):
        lokal=pk
        serwisy = DodajSerwis.objects.filter(naprawa=True).filter(sklep=lokal).order_by('-id')
        # serwisy = DodajSerwis.objects.all().order_by('-id')
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(serwisy, page_records)
        serwisy_pagi = paginator.get_page(page)
        lokale=Sklep.objects.all()
        
        ctx = {'serwisy': serwisy_pagi,'lokal':lokal,'lokale':lokale}
        return render(request, 'serwisy_filter.html', ctx)
    
    def post(self, request,pk):
        szukaj = request.POST.get('szukaj')
        
        serwisy_dostepne = DodajSerwis.objects.filter(archiwum=False)
        serwisy = serwisy_dostepne.filter(Q(id__icontains=szukaj) |
            Q(marka__nazwa__icontains=szukaj) | Q(model__icontains=szukaj)
            | Q(imei__icontains=szukaj))
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(serwisy, page_records)
        serwisy_pagi = paginator.get_page(page)
        ctx = {'serwisy': serwisy_pagi}
        return render(request, 'serwisy_filter.html', ctx)

    
@method_decorator(login_required, name='dispatch')
class ListaSerwisowGotowychMagazynView(PermissionRequiredMixin,View):
    permission_required='miktel.view_dodajserwis'
    def get(self, request):
        lokal=request.user.sklep_dzisiaj.id
        serwisy = DodajSerwis.objects.filter(status="4").filter(sklep=lokal).order_by('-id')
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(serwisy, page_records)
        serwisy_pagi = paginator.get_page(page)
        ctx = {'serwisy': serwisy_pagi,'lokal':lokal}
        return render(request, 'serwisy_gotowe.html', ctx)
    
    def post(self, request):
        szukaj = request.POST.get('szukaj')

        serwisy_dostepne = DodajSerwis.objects.filter(archiwum=False).filter(status=4)
        serwisy = serwisy_dostepne.filter(Q(id__icontains=szukaj) |
            Q(marka__nazwa__icontains=szukaj) | Q(model__icontains=szukaj)
            | Q(imei__icontains=szukaj))
        global page_records
        page = request.GET.get('page')
        paginator = Paginator(serwisy, page_records)
        serwisy_pagi = paginator.get_page(page)
        ctx = {'serwisy': serwisy_pagi}
        
        return TemplateResponse(request, 'serwisy_gotowe.html', ctx)

@method_decorator(login_required, name='dispatch')
class ListaSerwisowGotowychFilterMagazynView(PermissionRequiredMixin,View):
    permission_required='miktel.view_dodajserwis'
    def get(self, request,pk):
        lokal=pk
        serwisy = DodajSerwis.objects.filter(status="4").filter(sklep=lokal).order_by('-id')
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(serwisy, page_records)
        serwisy_pagi = paginator.get_page(page)
        ctx = {'serwisy': serwisy_pagi,'lokal':lokal}
        return render(request, 'serwisy_gotowe.html', ctx)
    
    def post(self, request,pk):
        szukaj = request.POST.get('szukaj')

        serwisy_dostepne = DodajSerwis.objects.filter(archiwum=False).filter(status=4)
        serwisy = serwisy_dostepne.filter(Q(id__icontains=szukaj) |
            Q(marka__nazwa__icontains=szukaj) | Q(model__icontains=szukaj)
            | Q(imei__icontains=szukaj))
        global page_records
        page = request.GET.get('page')
        paginator = Paginator(serwisy, page_records)
        serwisy_pagi = paginator.get_page(page)
        ctx = {'serwisy': serwisy_pagi}
        
        return TemplateResponse(request, 'serwisy_gotowe.html', ctx)


@method_decorator(login_required, name='dispatch')
class SzczegolySerwisuView(PermissionRequiredMixin,UpdateView):
    permission_required='miktel.change_dodajserwis'
    model = DodajSerwis
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/lista_serwisow/')


@method_decorator(login_required, name='dispatch')
class GotowySerwisView(PermissionRequiredMixin,View):
    permission_required='miktel.view_dodajserwis'
    def get(self, request, pk):
        serwis = DodajSerwis.objects.get(pk=pk)
        saldo = saldo_sms()
        ctx = {'serwis': serwis, 'saldo': saldo}
        return render(request, 'checking_service.html', ctx)


@method_decorator(login_required, name='dispatch')
class ServiceReadyView(PermissionRequiredMixin,View):
    permission_required='miktel.view_dodajserwis'
    def get(self, request, pk):
       
        service = DodajSerwis.objects.get(pk=pk)
        cena_zgoda = request.GET['cena']
        koszt = request.GET['koszt']
        info = request.GET['info']
        serwis_wlasny = request.GET['serwis_wlasny']
        premia = PremiaJob.objects.filter()
        pracownik=request.user
        
        if serwis_wlasny == "1":
            usluga = Usluga.objects.filter(czesci=True)
            premia = PremiaJob.objects.filter(usluga__in=usluga).filter(pracownik=request.user).last()
            if premia:
                if premia.check != service.id:
                    service.serwisant = pracownik
                    service.cena_zgoda = cena_zgoda
                    service.koszt = koszt
                    service.info = info
                    service.status = "4"
                    service.data_wydania=datetime.now()
                    service.naprawa = False
                    service.save()
            
                    PremiaJob.objects.create(check=service.id,
                                         model=service.model,
                                         sklep=request.user.sklep_dzisiaj,
                                         pracownik=request.user,
                                         usluga=service.usluga,
                                         cena_klient=cena_zgoda,
                                         koszt=koszt)
                
                    zysk = int(service.cena_zgoda) - int(service.koszt)
                    subject = "Pracownicy premiuja. Wykonano serwis wlasny w {}".format(
                    request.user.sklep_dzisiaj)
                    text = "{} {} zysk {}".format(service.usluga, service.model,
                                              zysk)
                    send_email(subject, text)
                    message = "Serwis gotowy do odbioru. Cena za naprawe to {}. Zapraszamy do punktu {}".format(
                    cena_zgoda, service.sklep)

                    if 'sms' in request.GET:
                        sms = request.GET['sms']
                        send(service.numer_telefonu, message)
                    else:
                        sms = False

                    return HttpResponseRedirect('/lista_serwisow/')
                else:
                    service.serwisant = pracownik
                    service.cena_zgoda = cena_zgoda
                    service.koszt = koszt
                    service.info = info
                    service.status = "4"
                    service.data_wydania=datetime.now()
                    service.naprawa = False
                    service.save()
                    if 'sms' in request.GET:
                        sms = request.GET['sms']
                        message = "Serwis gotowy do odbioru. Cena za naprawe to {}. Zapraszamy do punktu {}".format(
                        cena_zgoda, service.sklep)
                        send(service.numer_telefonu, message)
                    else:
                        sms = False
                    return HttpResponseRedirect('/lista_serwisow/')

            else:
                PremiaJob.objects.create(check=service.id,
                                         model=service.model,
                                         sklep=request.user.sklep_dzisiaj,
                                         pracownik=request.user,
                                         usluga=service.usluga,
                                         cena_klient=cena_zgoda,
                                         koszt=koszt)
                service.serwisant = pracownik
                service.cena_zgoda = cena_zgoda
                service.koszt = koszt
                service.info = info
                service.status = "4"
                service.data_wydania=datetime.now()
                service.naprawa = False
                service.save()
                
                zysk = int(service.cena_zgoda) - int(service.koszt)
                subject = "Pracownicy premiuja. Wykonano serwis wlasny w {}".format(
                request.user.sklep_dzisiaj)
                text = "{} {} zysk {}".format(service.usluga, service.model,
                                              zysk)
                send_email(subject, text)
                message = "Serwis gotowy do odbioru. Cena za naprawe to {}. Zapraszamy do punktu {}".format(
                cena_zgoda, service.sklep)

                if 'sms' in request.GET:
                    sms = request.GET['sms']
                    send(service.numer_telefonu, message)
                else:
                    sms = False

                    # send(service.numer_telefonu, message)
                return HttpResponseRedirect('/lista_serwisow/')

        else:
            service.serwisant = MyUser.objects.get(status_osoby=2)
            service.cena_zgoda = cena_zgoda
            service.koszt = koszt
            service.info = info
            service.status = "4"
            service.data_wydania=datetime.now()
            service.naprawa = False
            service.save()

            message = "Serwis gotowy do odbioru. Cena za naprawe to {}. Zapraszamy do punktu {}".format(
                cena_zgoda, service.sklep)
            if 'sms' in request.GET:
                sms = request.GET['sms']
                send(service.numer_telefonu, message)
            else:
                sms = False

                # send(service.numer_telefonu, message)
                # send_email(subject, text):
            return HttpResponseRedirect('/lista_serwisow/')


@method_decorator(login_required, name='dispatch')
class WydajSerwisView(PermissionRequiredMixin,View):
    permission_required='miktel.view_dodajserwis'
    def get(self, request, pk):
        serwis = DodajSerwis.objects.get(pk=pk)
        ctx = {'serwis': serwis}
        return render(request, 'checking2_service.html', ctx)

    def post(self, request, pk):
        service_id = request.POST['serwis_id']
        cena = request.POST['cena']
        premia=PremiaJob.objects.filter(check=service_id).first()
        service = DodajSerwis.objects.get(pk=service_id)
        
        if cena!=service.cena_zgoda:
            if premia!=None:
                premia.cena_klient=cena
                premia.save()
        service.cena_zgoda = cena
        service.status = "5"
        service.data_wydania = datetime.now()
        service.archiwum = True

        service.save()
        

        return redirect('/lista_serwisow_gotowych/')


@method_decorator(login_required, name='dispatch')
class ArchiwumSerwisView(PermissionRequiredMixin,View):
    permission_required='miktel.view_dodajserwis'
    def get(self, request):
        serwisy = DodajSerwis.objects.filter(archiwum=True).order_by('-id')
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(serwisy, page_records)
        serwisy_pagi = paginator.get_page(page)
        ctx = {'serwisy': serwisy_pagi,'page_records':page_records}
        return render(request, 'serwisy_archiwum.html', ctx)
    
    def post(self, request):
        szukaj = request.POST.get('szukaj')

        serwisy_dostepne = DodajSerwis.objects.filter(archiwum=True)
        serwisy = serwisy_dostepne.filter(Q(id__icontains=szukaj) |
            Q(marka__nazwa__icontains=szukaj) | Q(model__icontains=szukaj)
            | Q(imei__icontains=szukaj))
        
        ctx = {'serwisy': serwisy}
        return TemplateResponse(request, 'serwisy_archiwum.html', ctx)


@method_decorator(login_required, name='dispatch')
class ReklamacjaSerwisView(PermissionRequiredMixin,View):
    permission_required='miktel.view_dodajserwis'
    def get(self, request, pk):
        serwis = DodajSerwis.objects.get(pk=pk)
        serwis.archiwum = False
        serwis.data = datetime.now()
        serwis.status = "7"
        serwis.naprawa = True
        serwis.save()
        serwisy = DodajSerwis.objects.filter(archiwum=False)
        ctx = {'serwisy': serwisy}
        return redirect('/lista_serwisow/')



#SEKCJA CZEŚCI GSM
@method_decorator(login_required, name='dispatch')
class CzesciCreateView(PermissionRequiredMixin,View):
    permission_required='miktel.add_czesc'
    def get(self, request):
        form = CzescCreateForm()
        ctx = {'form': form}
        return render(request, 'czesc_form.html', ctx)

    def post(self, request):
        form = CzescCreateForm(request.POST)
        if form.is_valid():
            foto = form.cleaned_data['foto']
            typ = form.cleaned_data['typ']
            marka = form.cleaned_data['marka']
            stan = form.cleaned_data['stan']
            kolor = form.cleaned_data['kolor']
            nazwa = form.cleaned_data['nazwa']
            cena_zak = form.cleaned_data['cena_zak']
            cena_sprzed = form.cleaned_data['cena_sprzed']
            ilosc = form.cleaned_data['ilosc']
            opis = form.cleaned_data['opis']

            pracownik = request.user

            czesc = Czesc.objects.create(pracownik=pracownik,
                                         sklep=pracownik.sklep_dzisiaj,
                                         typ=typ,
                                         marka=marka,
                                         kolor=kolor,
                                         nazwa=nazwa,
                                         cena_zak=cena_zak,
                                         cena_sprzed=cena_sprzed,
                                         ilosc=ilosc,
                                         opis=opis)
            for el in foto:
                foto = Foto.objects.get(pk=el.id)
                foto.used=True
                czesc.foto.add(foto)
                czesc.save()
                foto.save()

            return HttpResponseRedirect('/lista_czesci/')
        else:
            print('Nie jest valid')
            return HttpResponseRedirect('')

@method_decorator(login_required, name='dispatch')
class ListaCzesciView(PermissionRequiredMixin,View):
    permission_required='miktel.view_czesc'
    def get(self, request):
        czesc = Czesc.objects.all()
        page = request.GET.get('page')
        global page_records
        paginator = Paginator(czesc, page_records)
        czesc_pagi = paginator.get_page(page)
        ctx = {"czesc": czesc_pagi}
        return render(request, 'lista_czesci.html', ctx)

    def post(self, request):
        szukaj = request.POST.get('szukaj')

        czesc = Czesc.objects.filter(
            Q(marka__nazwa__icontains=szukaj) | Q(nazwa__icontains=szukaj)
            | Q(typ__nazwa__icontains=szukaj)
            | Q(sklep__nazwa__icontains=szukaj))

        page = request.GET.get('page')
        global page_records
        paginator = Paginator(czesc, page_records)
        czesc_pagi = paginator.get_page(page)
        ctx = {"czesc": czesc_pagi, 'paginator': paginator}
        return render(request, 'lista_czesci.html', ctx)


@method_decorator(login_required, name='dispatch')
class AddMoreItemsView(PermissionRequiredMixin,View):
    permission_required='miktel.add_czesc'
    def get(self, request, pk):
        czesc = Czesc.objects.get(pk=pk)
        form = DodajWiecejCzesci()
        ctx = {'czesc': czesc, 'form': form}
        return render(request, 'dodaj_wiecej_czesci.html', ctx)
    
    def post(self, request, pk):
        form = DodajWiecejCzesci(request.POST)
        if form.is_valid():
            ilosc = form.cleaned_data['ilosc']

            czesc = Czesc.objects.get(pk=pk)
            czesc.dostepny=True
            quantity=czesc.ilosc
            czesc.ilosc=quantity+ilosc
            czesc.save()

            # page = request.GET.get('page')
            # paginator = Paginator(czesc, page_records)
            # czesc_pagi = paginator.get_page(page)
            # ctx = {"czesc": czesc_pagi}
            return HttpResponseRedirect('/lista_czesci/')

@method_decorator(login_required, name='dispatch')
class AddMoreItemsSimiliarView(PermissionRequiredMixin,View):
    permission_required='miktel.add_czesc'
    def get(self,request,pk):
        czesc = Czesc.objects.get(pk=pk)
        form = DodajWiecejCzesci_podbne()
        ctx = {'czesc': czesc, 'form': form}
        return render(request, 'dodaj_wiecej_czesci_podobnych.html', ctx)
    
    def post(self, request,pk):
        form = DodajWiecejCzesci_podbne(request.POST)
        if form.is_valid():
            czesc=Czesc.objects.get(pk=pk)
            foto = czesc.foto.all()
            marka=czesc.marka
            typ=czesc.typ
            nazwa=czesc.nazwa

            stan = form.cleaned_data['stan']
            kolor = form.cleaned_data['kolor']
            cena_zak = form.cleaned_data['cena_zak']
            cena_sprzed = form.cleaned_data['cena_sprzed']
            ilosc = form.cleaned_data['ilosc']
            opis = form.cleaned_data['opis']

            pracownik = request.user

            czesc = Czesc.objects.create(pracownik=pracownik,
                                         sklep=pracownik.sklep_dzisiaj,
                                         typ=typ,
                                         marka=marka,
                                         kolor=kolor,
                                         nazwa=nazwa,
                                         cena_zak=cena_zak,
                                         cena_sprzed=cena_sprzed,
                                         ilosc=ilosc,
                                         opis=opis)
            for el in foto:
                foto = Foto.objects.get(pk=el.id)
                czesc.foto.add(foto)
                czesc.save()

            return HttpResponseRedirect('/lista_czesci/')
        else:
            return render(request, "form_errors.html", context={'form': form})


@method_decorator(login_required, name='dispatch')
class RemoveMoreItemsView(PermissionRequiredMixin,View):
    permission_required='miktel.delete_czesc'
    def get(self, request, pk):
        czesc = Czesc.objects.get(pk=pk)
        form = UsunWiecejCzesci()
        ctx = {'czesc': czesc, 'form': form}
        return render(request, 'dodaj_wiecej_czesci.html', ctx)
    
    def post(self, request, pk):
        form = UsunWiecejCzesci(request.POST)
        if form.is_valid():
            ilosc = form.cleaned_data['ilosc']

            czesc = Czesc.objects.get(pk=pk)
            czesc.dostepny=True
            quantity=czesc.ilosc
            if quantity>ilosc:
                czesc.ilosc=quantity-ilosc
            else:
                czesc.ilosc=0
            czesc.save()

            # page = request.GET.get('page')
            # paginator = Paginator(czesc, page_records)
            # czesc_pagi = paginator.get_page(page)
            # ctx = {"czesc": czesc_pagi}
            return HttpResponseRedirect('/lista_czesci/')
        else:
            return render(request, "form_errors.html", context={'form': form})

@method_decorator(login_required, name='dispatch')
class SzczegolyCzesciView(PermissionRequiredMixin,UpdateView):
    permission_required='miktel.change_czesc'
    model = Czesc
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/lista_czesci/')


@method_decorator(login_required, name='dispatch')
class UzyjCzesciWieleView(PermissionRequiredMixin,View):
    permission_required='miktel.view_czesc'
    def post(self, request):
        form = CenaKlientForm()
        czesci_lista = request.POST.getlist('checks')
        query_list = []
        total_koszt = []
        
        if len(czesci_lista)>0:
            for el in czesci_lista:
                czesc = Czesc.objects.get(pk=el)
                marka_czesci = czesc.marka.id
                query_list.append(czesc)
                total_koszt.append(czesc.cena_zak)
            total = sum(total_koszt)
            saldo = saldo_sms()
            marka=Marka.objects.get(pk=marka_czesci)
            usluga = Usluga.objects.filter(czesci=True)
            serwisy = DodajSerwis.objects.filter(usluga__in=usluga).filter(
            naprawa=True).filter(marka=marka)
            ctx = {
            'form': form,
            'query_list': query_list,
            'total': total,
            'marka': marka,
            'serwisy': serwisy,
            'saldo': saldo,
            'czesci_lista': czesci_lista
             }
            return render(request, 'wydaj_serwis_czesci.html', ctx)
        else:    
            czesc = Czesc.objects.all()
            page = request.GET.get('page')
            paginator = Paginator(czesc, page_records)
            czesc_pagi = paginator.get_page(page)
            ctx = {"czesc": czesc_pagi}
            return render(request, 'lista_czesci2.html', ctx)


@method_decorator(login_required, name='dispatch')
class WydajSerwisCzesciView(PermissionRequiredMixin,View):
    permission_required='miktel.view_czesc'
    def post(self, request):
        czesci_lista = request.POST.getlist('checks')
        koszt = request.POST.get('koszt')
        serwis_id = request.POST.get('serwis_id')
        print(serwis_id)
        cena_zgoda = request.POST.get('cena_klient')

        total_koszt = []
        query_list = []

        usluga = Usluga.objects.filter(czesci=True)
        premia = PremiaJob.objects.filter(usluga__in=usluga).filter(pracownik=request.user).last()
        # print(premia.check)

        if serwis_id != "":
            serwis = DodajSerwis.objects.get(pk=serwis_id)
            if not premia:
                premia = PremiaJob.objects.create(
                    check=serwis_id,
                    sklep=request.user.sklep_dzisiaj,
                    pracownik=request.user,
                    usluga=serwis.usluga,
                    model=serwis.model,
                    cena_klient=cena_zgoda,
                    koszt=koszt)
                
                if len(czesci_lista) > 0:
                    for el in czesci_lista:
                        czesc = Czesc.objects.get(pk=el)
                        query_list.append(czesc)
                        total_koszt.append(czesc.cena_zak)
                        if czesc.ilosc > 0:
                            czesc.ilosc -= 1

                        marka = czesc.marka
                        czesc.save()
                        koszt = sum(total_koszt)
                else:
                    koszt = 0
                
                serwis.status = "4"
                serwis.data_wydania=datetime.now()
                serwis.naprawa = False
                serwis.serwisant = request.user
                serwis.save()
                zysk = int(cena_zgoda) - koszt

                subject = "Wykonano serwis i uzyto czesci w {} przez {}".format(
                    premia.sklep, premia.pracownik)
                text = "{} wykonał {} w {} za {} zysk {}".format(
                    premia.pracownik, premia.usluga, premia.model,
                    premia.cena_klient, zysk)
                send_email(subject, text)

            else:
                if int(premia.check) != int(serwis_id):
                    print("jestem tutuaj")
                    print(premia.check)
                    print(serwis_id)
                    premia = PremiaJob.objects.create(
                        check=serwis_id,
                        sklep=request.user.sklep_dzisiaj,
                        pracownik=request.user,
                        usluga=serwis.usluga,
                        model=serwis.model,
                        cena_klient=cena_zgoda,
                        koszt=koszt)
                    serwis.status="4"
                    serwis.data_wydania=datetime.now()
                    serwis.save()
                    if len(czesci_lista) > 0:
                        for el in czesci_lista:
                            czesc = Czesc.objects.get(pk=el)
                            query_list.append(czesc)
                            total_koszt.append(czesc.cena_zak)
                            if czesc.ilosc > 0:
                                czesc.ilosc -= 1

                            marka = czesc.marka
                            czesc.save()
                            koszt = sum(total_koszt)
                    else:
                        koszt = 0
                    serwis.status = "4"
                    serwis.data_wydania=datetime.now()
                    serwis.naprawa = False
                    serwis.serwisant = request.user
                    serwis.save()

            zysk = int(cena_zgoda) - int(koszt)

            message = "Serwis gotowy do odbioru. Cena za naprawe to {}. Zapraszamy do punktu {}".format(
            cena_zgoda, serwis.sklep)

            if 'sms' in request.POST:
                sms = request.POST['sms']
                send(serwis.numer_telefonu, message)
                print('Jesy sms')
            else:
                sms = False
                print('nie ma smsma')

            subject = "Wykonano serwis i uzyto czesci w {} przez {}".format(
                premia.sklep, premia.pracownik)
            text = "{} wykonał {} w {} za {} zysk {}".format(
                premia.pracownik, premia.usluga, premia.model,
                premia.cena_klient, zysk)
            send_email(subject, text)
            return HttpResponseRedirect('/lista_serwisow/')

        return HttpResponseRedirect('/RETURNERRORS/')

@method_decorator(login_required, name='dispatch')
class WydajSerwisCzesci2View(PermissionRequiredMixin,View):
    permission_required='miktel.view_czesc'
    def post(self, request):
        czesci_lista = request.POST.getlist('checks')
        koszt = request.POST.get('koszt')
        serwis_id = request.POST.get('serwis_id')
        print(serwis_id)
        cena_zgoda = request.POST.get('cena_klient')

        total_koszt = []
        query_list = []

        usluga = Usluga.objects.filter(czesci=True)
        premia = PremiaJob.objects.filter(usluga__in=usluga).last()
        # print(premia.check)

        if serwis_id != "":
            serwis = DodajSerwis.objects.get(pk=serwis_id)
            if not premia:
                # print("not")
                premia = PremiaJob.objects.create(
                    check=serwis_id,
                    sklep=request.user.sklep_dzisiaj,
                    pracownik=request.user,
                    usluga=serwis.usluga,
                    model=serwis.model,
                    cena_klient=cena_zgoda,
                    koszt=koszt)
                if len(czesci_lista) > 0:
                    for el in czesci_lista:
                        czesc = Czesc.objects.get(pk=el)
                        query_list.append(czesc)
                        total_koszt.append(czesc.cena_zak)
                        if czesc.ilosc > 0:
                            czesc.ilosc -= 1

                        marka = czesc.marka
                        czesc.save()
                        koszt = sum(total_koszt)
                else:
                    koszt = 0
                serwis.status = "4"
                serwis.data_wydania=datetime.now()
                serwis.naprawa = False
                serwis.serwisant = request.user
                serwis.save()
                zysk = int(cena_zgoda) - koszt

                subject = "Wykonano serwis i uzyto czesci w {} przez {}".format(
                    premia.sklep, premia.pracownik)
                text = "{} wykonał {} w {} za {} zysk {}".format(
                    premia.pracownik, premia.usluga, premia.model,
                    premia.cena_klient, zysk)
                send_email(subject, text)

            else:
                if int(premia.check) != int(serwis_id):
                    print("jestem tutuaj")
                    print(premia.check)
                    print(serwis_id)
                    premia = PremiaJob.objects.create(
                        check=serwis_id,
                        sklep=request.user.sklep_dzisiaj,
                        pracownik=request.user,
                        usluga=serwis.usluga,
                        model=serwis.model,
                        cena_klient=cena_zgoda,
                        koszt=koszt)

                    if len(czesci_lista) > 0:
                        for el in czesci_lista:
                            czesc = Czesc.objects.get(pk=el)
                            query_list.append(czesc)
                            total_koszt.append(czesc.cena_zak)
                            if czesc.ilosc > 0:
                                czesc.ilosc -= 1

                            marka = czesc.marka
                            czesc.save()
                            koszt = sum(total_koszt)
                    else:
                        koszt = 0
                    serwis.status = "4"
                    serwis.data_wydania=datetime.now()
                    serwis.naprawa = False
                    serwis.serwisant = request.user
                    serwis.save()

                    zysk = int(cena_zgoda) - koszt

                    subject = "Wykonano serwis i uzyto czesci w {} przez {}".format(
                        premia.sklep, premia.pracownik)
                    text = "{} wykonał {} w {} za {} zysk {}".format(
                        premia.pracownik, premia.usluga, premia.model,
                        premia.cena_klient, zysk)
                    send_email(subject, text)
            return HttpResponseRedirect('/lista_serwisow/')

        return HttpResponseRedirect('/RETURNERRORS/')


@method_decorator(login_required, name='dispatch')
class GetServiceForItems(PermissionRequiredMixin,View):
    permission_required='miktel.view_czesc'
    def get(self, request, pk):
        service = DodajSerwis.objects.get(pk=pk)
        marka = service.marka
        items = Czesc.objects.filter(marka=marka)
        page = request.GET.get('page')
        paginator = Paginator(items, page_records)
        items_pagi = paginator.get_page(page)
        ctx = {'serwis': service,"czesc": items_pagi}
        return render(request, 'lista_czesci_serwis.html', ctx)

@method_decorator(login_required, name='dispatch')
class UzyjCzesciSerwisView(PermissionRequiredMixin,View):
    permission_required='miktel.view_czesc'
    def post(self, request):
        form = CenaKlientForm()
        czesci_lista = request.POST.getlist('checks')
        serwis_id = request.POST.get('serwis_id')
        serwis=DodajSerwis.objects.get(pk=serwis_id)

        query_list = []
        total_koszt = []
        for el in czesci_lista:
            czesc = Czesc.objects.get(pk=el)
            marka_czesci = czesc.marka.id
            query_list.append(czesc)
            total_koszt.append(czesc.cena_zak)
        total = sum(total_koszt)
        saldo = saldo_sms()
        marka = Marka.objects.get(pk=marka_czesci)
        # print(marka)
        usluga = Usluga.objects.filter(czesci=True)
        serwisy = DodajSerwis.objects.filter(usluga__in=usluga).filter(
            naprawa=True).filter(marka=marka)
        ctx = {
            'form': form,
            'query_list': query_list,
            'total': total,
            'marka': marka,
            'serwis': serwis,
            'saldo': saldo,
            'czesci_lista': czesci_lista
        }
        return render(request, 'wydaj_serwis_czesci2.html', ctx)



#SEKCJA PREMIOWANIE
@method_decorator(login_required, name='dispatch')
class DodajPremiaJobView(PermissionRequiredMixin,View):
    permission_required='miktel.view_premiajob'
    def get(self, request):
        form=AddJobForm()
        pracownik = request.user
        # print(pracownik.id)
        sklepy = pracownik.sklep.all()
        dlugosc = len(pracownik.sklep.all())
        uslugi = Usluga.objects.filter(sklep__in=sklepy).filter(
            zakup=False).filter(sprzedaz=False).filter(czesci=False).filter(akcesoria=False).order_by('nazwa')
        uslugi_unique = []
        for el in uslugi:
            if el not in uslugi_unique:
                uslugi_unique.append(el)
        # dlugosc = len(pracownik.sklep.all())
        # telefony = Telefon.objects.filter(
        #     sklep__in=sklepy).order_by('marka').order_by('nazwa')

        ctx = {'form':form,
            'pracownik': pracownik,
            # 'sklepy': sklepy,
            'uslugi': uslugi_unique
        }
        return TemplateResponse(request, "add_usluga.html", ctx)

    def post(self, request):
        form = AddJobForm(request.POST)
        if form.is_valid():
            pracownik = request.user
            usluga = request.POST.get('usluga')
            model = request.POST.get('model')
            sklep = request.user.sklep_dzisiaj
            usluga_instance = Usluga.objects.get(pk=usluga)
            cena = request.POST.get('cena_klient')
            koszt = request.POST.get('koszt')

            PremiaJob.objects.create(model=model,
                                 sklep=sklep,
                                 pracownik=pracownik,
                                 usluga=usluga_instance,
                                 cena_klient=cena,
                                 koszt=koszt)

            subject = "Wykonano usługe {} w {}".format(usluga_instance, sklep)
            text = "{} wykonał {} {} za {}, koszt {} ".format(
            pracownik, usluga_instance, model, cena, koszt)
            # send_email(subject, text)
            return redirect('szczegoly_serwisow_serwisanta', pracownik.id, miesiac,
                        rok)


@method_decorator(login_required, name='dispatch')
class DodajInnePraceView(PermissionRequiredMixin,View):
    permission_required='miktel.view_innepracepremiowane'
    def get(self, request):
        form=InnePraceForm()
        return TemplateResponse(request, "add_usluga_inne.html", {'form':form})
    def post(self,request):
        form = InnePraceForm(request.POST)
        if form.is_valid():
            pracownik = request.user
            nazwa = request.POST.get('nazwa')
            czas = request.POST.get('czas')
            opis = request.POST.get('opis')
            sklep=request.user.sklep_dzisiaj
            premia=InnePracePremiowane.objects.create(nazwa=nazwa, czas=czas, opis=opis, pracownik=pracownik)

            return redirect('/twoje_premie/')
        else:
            return render(request, "form_errors.html", context={'form': form})


@method_decorator(login_required, name='dispatch')
class TwojePremieJobView(PermissionRequiredMixin,View):
    permission_required='miktel.view_premiajob'
    def get(self, request):
        pracownik = request.user
        data = MIESIACE[miesiac - 1][1]
       
        usluga_akc=Usluga.objects.get(akcesoria=True)
        akcesoria=PremiaJob.objects.filter(
            data__year=rok,
            data__month=miesiac).filter(pracownik=pracownik).filter(usluga=usluga_akc)
        usluga_serwis=Usluga.objects.filter(akcesoria=False)

        suma_akc = []
        premia_akc = []
        if len(akcesoria)>0:
            for el in akcesoria:
                if el.cena_klient>0:
                    suma_akc.append(el.cena_klient)
                    suma_all_akc = sum(suma_akc)
                    premia_result_akc = suma_all_akc*(el.usluga.kwota) / 100
                else:
                    premia_result_akc=0
        else:
            premia_result_akc=0
            suma_all_akc=0
        # zysk_netto_akc = suma_zysk_akc - premia_result
        
        uslugi = PremiaJob.objects.filter(
            data__year=rok,
            data__month=miesiac).filter(pracownik=pracownik).filter(usluga__in=usluga_serwis).order_by('-id')
        inne=InnePracePremiowane.objects.filter(
            data__year=rok,
            data__month=miesiac).filter(pracownik=pracownik).order_by('-id')
        zysk = []
        premia = []
        for el in uslugi:
            print(el.model)
            if el.cena_klient is not None and el.koszt is not None:
                zysk.append(el.cena_klient-el.koszt)
                if el.usluga.typ == 0:
                    if el.cena_klient>=el.koszt: 
                        premia.append(((el.cena_klient - el.koszt) *
                                   (el.usluga.kwota)) / 100)
                        print("pierwszy if")
                        print(premia)
                        print(el.usluga.typ)
                    else:
                        premia.append(0)
                else:
                    premia.append(el.usluga.kwota)
                    
        for el in premia:
            print(el) 
              
                

        suma_zysk = round(sum(zysk,2))
        premia_result = round(sum(premia), 2)
        zysk_netto = round((suma_zysk - premia_result),2)
        
        miesiace = MIESIACE
        rok_lista = ROK
        ctx = {
            'akcesoria':akcesoria,
            'suma_all_akc':suma_all_akc,
            'premia_result_akc':premia_result_akc,
            'uslugi': uslugi,
            'inne':inne,
            'pracownik': pracownik,
            'miesiac': miesiac,
            'miesiace':miesiace,
            'data': data,
            'rok': rok,
            'rok_lista':rok_lista,
            'zysk': suma_zysk,
            'premia': format(premia_result, '.2f'),
            'zysk_netto': format(zysk_netto, '.2f'),
        }
        return TemplateResponse(request, "szczegoly_serwisow_serwisanta.html",
                                ctx)
    def post(self, request):
        miesiac_filter = request.POST.get('miesiac')
        rok_filter = request.POST.get('rok')
        pracownik=request.user
        data = MIESIACE[miesiac - 1][1]
        print(miesiac)
        print(rok)

        usluga_akc=Usluga.objects.get(akcesoria=True)
        akcesoria=PremiaJob.objects.filter(
            data__year=rok_filter,
            data__month=miesiac_filter).filter(pracownik=pracownik).filter(usluga=usluga_akc)
        
        suma_all_akc=0
        premia_result_akc=0
        suma_akc = []
        premia_akc = []
        for el in akcesoria:
            if el.cena_klient is not None and el.koszt is not None:
                suma_akc.append(el.cena_klient)

                suma_all_akc = sum(suma_akc)
                premia_result_akc = suma_all_akc*(el.usluga.kwota) / 100
            
                
        usluga_serwis=Usluga.objects.filter(akcesoria=False)
        uslugi = PremiaJob.objects.filter(
            data__year=rok_filter,
            data__month=miesiac_filter).filter(pracownik=pracownik).filter(usluga__in=usluga_serwis).order_by('-id')
        
        
        zysk = []
        premia = []
        for el in uslugi:
            print(el.model)
            if el.cena_klient is not None and el.koszt is not None:
                zysk.append(el.cena_klient-el.koszt)
                if el.usluga.typ == 0:
                    if el.cena_klient>=el.koszt: 
                        premia.append(((el.cena_klient - el.koszt) *
                                   (el.usluga.kwota)) / 100)
                        print("pierwszy if")
                        print(premia)
                        print(el.usluga.typ)
                    else:
                        premia.append(0)
                else:
                    premia.append(el.usluga.kwota)

        suma_zysk = sum(zysk)
        premia_result = sum(premia)
        zysk_netto = suma_zysk - premia_result

        inne=InnePracePremiowane.objects.filter(
            data__year=rok_filter,
            data__month=miesiac_filter).filter(pracownik=pracownik).order_by('-id')
        
        miesiace = MIESIACE
        rok_lista = ROK
        ctx = {
            'akcesoria':akcesoria,
            'suma_all_akc':suma_all_akc,
            'premia_result_akc':premia_result_akc,
            'uslugi': uslugi,
            'inne':inne,
            'pracownik': pracownik,
            'miesiac': miesiac,
            'miesiace':miesiace,
            'data': data,
            'rok': rok,
            'rok_lista':rok_lista,
            'zysk': suma_zysk,
            'premia':format(premia_result, '.2f'),
            'zysk_netto': format(zysk_netto, '.2f'),
        }
        return TemplateResponse(request, "szczegoly_serwisow_serwisanta.html",ctx)

@method_decorator(login_required, name='dispatch')
class DodajAkcesoriaView(PermissionRequiredMixin,View):
    permission_required='miktel.view_usluga'
    def get(self, request):
        form=DodajAkcesoriaForm()
        ctx = {'form':form,
        }
        return TemplateResponse(request, "add_akcesoria.html", ctx)
    
    def post(self, request):
        form = DodajAkcesoriaForm(request.POST)
        if form.is_valid():
            pracownik = request.user
            usluga = Usluga.objects.get(akcesoria=True)
            miesiac = request.POST.get('miesiac')
            cena = request.POST.get('cena_klient')
            model = "Sprzedaż akcesoriów"
            sklep = request.user.sklep_dzisiaj
            koszt = 0
            data=str(rok)+"-"+str(miesiac)+"-"+str(1)

            premia_akc=PremiaJob.objects.create(model=model,
                                 sklep=sklep,
                                 pracownik=pracownik,
                                 usluga=usluga,
                                 cena_klient=cena,
                                 koszt=koszt,data=data)
            premia_akc.data=data
            premia_akc.save()
            subject = "Pracownik {} sprzedał akcesoria na kwotę {} w miesiącu {}".format(pracownik,cena_klient,usluga, miesiac)
            text = "{} wykonał {} {} za {}, koszt {} ".format(
            pracownik, usluga, model, cena, koszt)
            # send_email(subject, text)
            return redirect('twoje_premieJob')
        else:
            return render(request, "form_errors.html", context={'form': form})


@method_decorator(login_required, name='dispatch')
class EdycjaPremiaJobView(PermissionRequiredMixin,UpdateView):
    permission_required='miktel.change_premiajob'
    model = PremiaJob
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/dashboard_sklepow/')



@method_decorator(login_required, name='dispatch')
class DashboardView(PermissionRequiredMixin,View):
    permission_required='miktel.change_premiajob'
    def get(self, request):
        miesiace = MIESIACE
        rok = ROK
        sklepy = Sklep.objects.all()
        ctx = {'miesiace': miesiace, 'rok': ROK, 'sklepy': sklepy}
        return TemplateResponse(request, "filtruj_wg_daty.html", ctx)

    def post(self, request):
        miesiac = request.POST.get('miesiac')
        rok = request.POST.get('rok')
        sklep = request.POST.get('sklep')
        sklep_instacja = Sklep.objects.get(id=sklep)

        uslugi = PremiaJob.objects.filter(
            data__year=rok, data__month=miesiac).filter(sklep=sklep)

        pracownicy = MyUser.objects.filter(sklep=sklep)
        typ_uslugi = Usluga.objects.filter(sklep=sklep)
        counter = PremiaJob.objects.filter(data__year=rok,
                                           data__month=miesiac).count
        
        serwisy_wydane=DodajSerwis.objects.filter(sklep=sklep).filter(status="5").filter(data_wydania__year=rok,
                                           data_wydania__month=miesiac)
        
        serwisy_wydane_licznik=serwisy_wydane.count
        serwisy_wydane_zysk=0
        for el in serwisy_wydane:
            serwisy_wydane_zysk+=el.cena_zgoda-el.koszt
        
        umowy_komisowe=UmowaKomisowaNew.objects.filter(sklep_zak=sklep).filter(data_zak__year=rok,
                                           data_zak__month=miesiac).count
        telefony_sprzedane=Telefon.objects.filter(sklep_sprzed=sklep).filter(data_sprzed__year=rok,
                                           data_sprzed__month=miesiac).count
        telefony_sprzedane_zysk=Telefon.objects.filter(sklep_sprzed=sklep).filter(data_sprzed__year=rok,
                                           data_sprzed__month=miesiac)
        usługi=PremiaJob.objects.filter(sklep=sklep).filter(data__year=rok,
                                           data__month=miesiac)
        usługi_licznik=uslugi.count
        telefony_zysk=0
        for el in telefony_sprzedane_zysk:
            telefony_zysk+=el.cena_sprzed-el.cena_zak
        
        premia_jobs_suma=uslugi
        suma_premia_jobs = 0
        for el in premia_jobs_suma:
            if el.usluga.typ == 0:
                suma_premia_jobs += (el.cena_klient - el.koszt) * (
                    (el.usluga.kwota)) / 100
            else:
                suma_premia_jobs += el.usluga.kwota

        zysk_z_premia_jobs=0
        for el in premia_jobs_suma:
            if el.cena_klient > el.koszt:
                zysk_z_premia_jobs += el.cena_klient - el.koszt
        
        zysk_z_premia_jobs_serwis=0
        usluga_serwis=Usluga.objects.filter(czesci=True)
        for el in premia_jobs_suma:
            if el.usluga in usluga_serwis:
                zysk_z_premia_jobs_serwis += el.cena_klient - el.koszt
        
        zysk_z_premia_jobs_grawer=0
        usluga_grawer=Usluga.objects.filter(grawer=True)
        for el in premia_jobs_suma:
            if el.usluga in usluga_grawer:
                zysk_z_premia_jobs_grawer += el.cena_klient - el.koszt


        for pracownik in pracownicy:
            pracownik.licznik(uslugi)

        ctx = {
            'serwisy_wydane_licznik':serwisy_wydane_licznik,
            'serwisy_wydane_zysk':round(serwisy_wydane_zysk,2),
            'umowy_komisowe':umowy_komisowe,
            'telefony_sprzedane':telefony_sprzedane,
            'telefony_zysk':telefony_zysk,
            'usługi_licznik':usługi_licznik,
            'suma_premia_jobs':round(suma_premia_jobs,2),
            'zysk_z_premia_jobs':round(zysk_z_premia_jobs,2),
            'zysk_z_premia_jobs_serwis':round(zysk_z_premia_jobs_serwis,2),
            'zysk_z_premia_jobs_grawer':round(zysk_z_premia_jobs_grawer,2),
            'sklep': sklep_instacja,
            'uslugi': uslugi,
            'pracownicy': pracownicy,
            'miesiac': miesiac,
            'rok': rok,
            'typ': typ_uslugi
        }
        return TemplateResponse(request, "dashboard_sklepow.html", ctx)

@method_decorator(login_required, name='dispatch')
class SzczegolySerwisySerwisantaView(PermissionRequiredMixin,View):
    permission_required='miktel.view_premiajob'
    def get(self, request,pk,miesiac,rok):
        pracownik = MyUser.objects.get(pk=pk)
        miesiac=miesiac
        rok=rok
        data = MIESIACE[miesiac - 1][1]
       
        usluga_akc=Usluga.objects.get(akcesoria=True)
        akcesoria=PremiaJob.objects.filter(
            data__year=rok,
            data__month=miesiac).filter(pracownik=pracownik).filter(usluga=usluga_akc)
        usluga_serwis=Usluga.objects.filter(akcesoria=False)

        suma_akc = []
        premia_akc = []
        if len(akcesoria)>0:
            for el in akcesoria:
                if el.cena_klient>0:
                    suma_akc.append(el.cena_klient)
                    suma_all_akc = sum(suma_akc)
                    premia_result_akc = suma_all_akc*(el.usluga.kwota) / 100
                else:
                    premia_result_akc=0
        else:
            premia_result_akc=0
            suma_all_akc=0
        # zysk_netto_akc = suma_zysk_akc - premia_result
        
        uslugi = PremiaJob.objects.filter(
            data__year=rok,
            data__month=miesiac).filter(pracownik=pracownik).filter(usluga__in=usluga_serwis).order_by('-id')
        inne=InnePracePremiowane.objects.filter(
            data__year=rok,
            data__month=miesiac).filter(pracownik=pracownik).order_by('-id')
        zysk = []
        premia = []
        for el in uslugi:
            print(el.model)
            if el.cena_klient is not None and el.koszt is not None:
                zysk.append(el.cena_klient-el.koszt)
                if el.usluga.typ == 0:
                    if el.cena_klient>=el.koszt: 
                        premia.append(((el.cena_klient - el.koszt) *
                                   (el.usluga.kwota)) / 100)
                        print("pierwszy if")
                        print(premia)
                        print(el.usluga.typ)
                    else:
                        premia.append(0)
                else:
                    premia.append(el.usluga.kwota)
                    
        for el in premia:
            print(el) 
              
                

        suma_zysk = sum(zysk)
        premia_result = sum(premia)
        zysk_netto = suma_zysk - premia_result
        
        miesiace = MIESIACE
        rok_lista = ROK
        ctx = {
            'akcesoria':akcesoria,
            'suma_all_akc':suma_all_akc,
            'premia_result_akc':premia_result_akc,
            'uslugi': uslugi,
            'inne':inne,
            'pracownik': pracownik,
            'miesiac': miesiac,
            'miesiace':miesiace,
            'data': data,
            'rok': rok,
            'rok_lista':rok_lista,
            'zysk': suma_zysk,
            'premia': format(premia_result, '.2f'),
            'zysk_netto': format(zysk_netto, '.2f'),
        }
        return TemplateResponse(request, "szczegoly_serwisow_serwisanta.html",
                                ctx)
    def post(self, request,pk,miesiac,rok):
        pracownik = MyUser.objects.get(pk=pk)
        miesiac_filter = request.POST.get('miesiac')
        rok_filter = request.POST.get('rok')
        pracownik=request.user
        data = MIESIACE[miesiac - 1][1]
        print(miesiac)
        print(rok)

        usluga_akc=Usluga.objects.get(akcesoria=True)
        akcesoria=PremiaJob.objects.filter(
            data__year=rok_filter,
            data__month=miesiac_filter).filter(pracownik=pracownik).filter(usluga=usluga_akc)
        
        suma_all_akc=0
        premia_result_akc=0
        suma_akc = []
        premia_akc = []
        for el in akcesoria:
            if el.cena_klient is not None and el.koszt is not None:
                suma_akc.append(el.cena_klient)

                suma_all_akc = sum(suma_akc)
                premia_result_akc = suma_all_akc*(el.usluga.kwota) / 100
            
                
        usluga_serwis=Usluga.objects.filter(akcesoria=False)
        uslugi = PremiaJob.objects.filter(
            data__year=rok_filter,
            data__month=miesiac_filter).filter(pracownik=pracownik).filter(usluga__in=usluga_serwis).order_by('-id')
        
        
        zysk = []
        premia = []
        for el in uslugi:
            print(el.model)
            if el.cena_klient is not None and el.koszt is not None:
                zysk.append(el.cena_klient-el.koszt)
                if el.usluga.typ == 0:
                    if el.cena_klient>=el.koszt: 
                        premia.append(((el.cena_klient - el.koszt) *
                                   (el.usluga.kwota)) / 100)
                        print("pierwszy if")
                        print(premia)
                        print(el.usluga.typ)
                    else:
                        premia.append(0)
                else:
                    premia.append(el.usluga.kwota)

        suma_zysk = sum(zysk)
        premia_result = sum(premia)
        zysk_netto = suma_zysk - premia_result

        inne=InnePracePremiowane.objects.filter(
            data__year=rok_filter,
            data__month=miesiac_filter).filter(pracownik=pracownik).order_by('-id')
        
        miesiace = MIESIACE
        rok_lista = ROK
        ctx = {
            'akcesoria':akcesoria,
            'suma_all_akc':suma_all_akc,
            'premia_result_akc':premia_result_akc,
            'uslugi': uslugi,
            'inne':inne,
            'pracownik': pracownik,
            'miesiac': miesiac,
            'miesiace':miesiace,
            'data': data,
            'rok': rok,
            'rok_lista':rok_lista,
            'zysk': suma_zysk,
            'premia': format(premia_result, '.2f'),
            'zysk_netto': format(zysk_netto, '.2f'),
        }
        return TemplateResponse(request, "szczegoly_serwisow_serwisanta.html",ctx)



  


#SECKJA ADMINISTRACJI 
@method_decorator(login_required, name='dispatch')
class DodajUslugaView(PermissionRequiredMixin,CreateView):
    permission_required='miktel.add_usluga'
    model = Usluga
    fields = '__all__'
    success_url = reverse_lazy("lista_uslug")


@method_decorator(login_required, name='dispatch')
class DodajFotoView(PermissionRequiredMixin,CreateView):
    permission_required='miktel.add_foto'
    model = Foto
    fields = '__all__'
    success_url = reverse_lazy("lista_uslug")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fotos = Foto.objects.all()
        context['fotos'] = fotos
        return context

@method_decorator(login_required, name='dispatch')
class EdycjaUslugiView(PermissionRequiredMixin,UpdateView):
    permission_required='miktel.change_usluga'
    model = Usluga
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/lista_uslug/')

@method_decorator(login_required, name='dispatch')
class ListaSklepowView(PermissionRequiredMixin,View):
    permission_required='miktel.view_sklep'
    def get(self, request):
        sklep=Sklep.objects.all()
        ctx={'sklepy':sklep}
        
        return TemplateResponse(request, "lista_sklepow.html", ctx)
        return render(request, '', ctx)


@method_decorator(login_required, name='dispatch')
class EdycjaSklepuView(PermissionRequiredMixin,UpdateView):
    permission_required='miktel.change_sklep'
    model = Sklep
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/lista_sklepow/')

@method_decorator(login_required, name='dispatch')
class DeleteUslugaView(PermissionRequiredMixin,DeleteView):
    permission_required='miktel.delete_usluga'
    model = Usluga
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/lista_uslug/')

@method_decorator(login_required, name='dispatch')
class ListaUslugView(PermissionRequiredMixin,View):
    permission_required='miktel.view_usluga'
    def get(self, request):
        usluga = Usluga.objects.all().order_by('-id')
        sklep = Sklep.objects.all().order_by('nazwa')

        uslugi_unique = []
        for el in usluga:
            if el not in uslugi_unique:
                uslugi_unique.append(el)
        ctx = {'usluga': uslugi_unique, 'sklepy': sklep}
        return render(request, 'lista_uslug.html', ctx)

@method_decorator(login_required, name='dispatch')
class AddShopView(PermissionRequiredMixin,CreateView):
    permission_required='miktel.add_sklep'
    model = Sklep
    fields = '__all__'
    success_url = reverse_lazy("widok_klienta")

@method_decorator(login_required, name='dispatch')
class AddTypeItemView(PermissionRequiredMixin,CreateView):
    permission_required = 'miktel.add_typ'
    raise_exception = True
    permission_denied_message = 'Permission Denied'
    
    model = Typ
    fields = '__all__'
    success_url = reverse_lazy("widok_klienta")

@method_decorator(login_required, name='dispatch')
class AddCompanyView(PermissionRequiredMixin,CreateView):
    permission_required = 'miktel.add_marka'
    raise_exception = True
    permission_denied_message = 'Permission Denied'
    model = Marka
    fields = '__all__'
    success_url = reverse_lazy("widok_klienta")

@method_decorator(login_required, name='dispatch')
class AddCategoryView(PermissionRequiredMixin,CreateView):
    permission_required='miktel.add_kategoria'
    model = Kategoria
    fields = '__all__'
    success_url = reverse_lazy("widok_klienta")
    
@method_decorator(login_required, name='dispatch')
class AddAdresView(PermissionRequiredMixin,CreateView):
    permission_required='miktel.add_adres'
    model = Adres
    fields = '__all__'
    success_url = reverse_lazy("widok_klienta")

@method_decorator(login_required, name='dispatch')
class AddHurtowniaView(PermissionRequiredMixin,CreateView):
    permission_required='miktel.add_hurtownia'
    model = Hurtownia
    fields = '__all__'
    success_url = reverse_lazy("widok_klienta")


@method_decorator(login_required, name='dispatch')
class DodajTypView(PermissionRequiredMixin,CreateView):
    model = Typ
    fields = '__all__'
    success_url = reverse_lazy("lista_typ")


@method_decorator(login_required, name='dispatch')
class TypView(PermissionRequiredMixin,CreateView):
    def get(self, request):
        typ = Typ.objects.all()
        ctx = {"typ": typ}
        return render(request, 'lista_typ.html', ctx)























# @method_decorator(login_required, name='dispatch')
# class TelefonView(CreateView):
#     model = Telefon
#     form_class = TelefonCreateForm
#     success_url = reverse_lazy("telefony_magazyn")

# def form_valid(self, form):
#     pracownik = self.request.user
#     Telefon = form.save(commit=False)
#     Telefon.sklep = Sklep.objects.get(pk=1)
#     return super().form_valid(form)
