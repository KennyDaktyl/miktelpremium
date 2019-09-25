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
page_records = 2
# Create your views here.


class MainView(View):
    def get(self, request):
        return TemplateResponse(request, "base.html")


@method_decorator(login_required, name='dispatch')
class TelefonyMagazynView(View):
    def get(self, request):
        telefony = Telefon.objects.filter(dostepny=True).order_by(
            'marka', 'nazwa', 'cena_sprzed')
        faktury = FakturaZakupu.objects.filter(telefon__in=telefony)
        umowy = UmowaKomisowaNew.objects.filter(phones__in=telefony)

        page = request.GET.get('page')
        paginator = Paginator(telefony, page_records)
        telefony_pagi = paginator.get_page(page)

        ctx = {
            'telefony': telefony_pagi,
            'faktury': faktury,
            'umowy': umowy,
            'paginator': paginator
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
        print(faktury)
        page = request.GET.get('page')
        paginator = Paginator(telefony, page_records)
        telefony_pagi = paginator.get_page(page)

        ctx = {
            'telefony': telefony_pagi,
            'faktury': faktury,
            'umowy': umowy,
            'paginator': paginator
        }
        return TemplateResponse(request, "telefony_magazyn.html", ctx)


@method_decorator(login_required, name='dispatch')
class SellPhonesView(View):
    def get(self, request, pk):
        telefon = Telefon.objects.get(pk=pk)
        faktura = FakturaZakupu.objects.all()
        umowa = UmowaKomisowaNew.objects.filter(phones=pk)
        print(len(umowa))
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
class TelefonySprzedaneView(View):
    def get(self, request):
        telefony = Telefon.objects.filter(dostepny=False).order_by(
            'marka', 'nazwa', 'cena_sprzed')
        faktury = FakturaZakupu.objects.filter(telefon__in=telefony)
        umowy = UmowaKomisowaNew.objects.filter(phones__in=telefony)
        page = request.GET.get('page')
        paginator = Paginator(telefony, page_records)
        telefony_pagi = paginator.get_page(page)

        ctx = {'telefony': telefony_pagi, 'faktury': faktury, 'umowy': umowy}
        return TemplateResponse(request, "telefony_sprzedane.html", ctx)

    def post(self, request):
        szukaj = request.POST.get('szukaj')

        Telefony_dostepne = Telefon.objects.filter(dostepny=False)
        telefony = Telefony_dostepne.filter(
            Q(marka__nazwa__icontains=szukaj) | Q(nazwa__icontains=szukaj)
            | Q(kategoria__nazwa__icontains=szukaj)
            | Q(imei__icontains=szukaj))
        faktury = FakturaZakupu.objects.filter(telefon__in=telefony)
        umowy = UmowaKomisowaNew.objects.filter(phones__in=telefony)
        print(faktury)
        ctx = {'telefony': telefony, 'faktury': faktury, 'umowy': umowy}
        return TemplateResponse(request, "telefony_sprzedane.html", ctx)


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

                # print(request.session['sklep_sesja'])
                # send('506029980', 'Zalogowano')
                # print(send)
                return redirect('/')
            else:
                return HttpResponse('Użytkownik {username} niepoprawny')
        return render(request, "/user_login.html", context={'form': form})


@login_required
def User_Logout(request):
    logout(request)

    return redirect('/')


# @method_decorator(login_required, name='dispatch')

@method_decorator(login_required, name='dispatch')
class AddShopView(CreateView):
    model = Sklep
    fields = '__all__'
    success_url = reverse_lazy("widok_klienta")

@method_decorator(login_required, name='dispatch')
class DodajMyUserView(CreateView):
    model = MyUser
    fields = '__all__'
    success_url = reverse_lazy("widok_klienta")

@method_decorator(login_required, name='dispatch')
class AddTypeItemView(CreateView):
    model = Typ
    fields = '__all__'
    success_url = reverse_lazy("widok_klienta")

@method_decorator(login_required, name='dispatch')
class AddCompanyView(CreateView):
    model = Marka
    fields = '__all__'
    success_url = reverse_lazy("widok_klienta")


@method_decorator(login_required, name='dispatch')
class ListaMyUserView(View):
    def get(self, request):
        pracownicy = MyUser.objects.all().order_by('last_name')
        ctx = {'pracownicy': pracownicy}
        return render(request, 'lista_pracownikow.html', ctx)


@method_decorator(login_required, name='dispatch')
class EdycjaMyUserView(UpdateView):
    model = MyUser
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/lista_uzytkownikow/')


@method_decorator(login_required, name='dispatch')
class ProfilView(View):
    def get(self, request, pk):
        pracownik = request.user
        sklepy = pracownik.sklep.all()
        # print(sklepy)
        ctx = {'sklepy': sklepy}
        return TemplateResponse(request, "profil_user.html", ctx)

    def post(self, request, pk):
        pracownik = request.user
        sklepy = pracownik.sklep.all()

        sklep_sesja = request.POST.get('sklep_sesja')
        if sklep_sesja != "":
            sklep_instancja = Sklep.objects.get(pk=sklep_sesja)
            user = MyUser.objects.get(pk=pracownik.id)
            user.sklep_dzisiaj = sklep_instancja
            user.save()
            request.user.sklep_dzisiaj = sklep_instancja

        ctx = {'sklepy': sklepy}
        return TemplateResponse(request, "profil_user.html", ctx)


@method_decorator(login_required, name='dispatch')
class UmowaKomisowaView(View):
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
            telefon_instancja.save()
            return HttpResponseRedirect('/checking_document/')
        else:
            print('Nie jest valid')
        return HttpResponseRedirect('/checking_document/')


@method_decorator(login_required, name='dispatch')
class CheckingDocumentView(View):
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

            return HttpResponseRedirect('/lista_umow/')

        else:
            if int(premia.check) != int(tele_id):
                print("rozne id")
                print(premia.check)
                print(tele_id)
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
                # send_email(subject, text)
                return HttpResponseRedirect('/lista_umow/')
            else:
                return HttpResponseRedirect('/lista_umow/')


@method_decorator(login_required, name='dispatch')
class EdycjaUmowyView(UpdateView):
    model = UmowaKomisowaNew
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/lista_umow/')


@method_decorator(login_required, name='dispatch')
class DeleteDocumentView(View):
    def get(self, request, pk):
        umowa = UmowaKomisowaNew.objects.get(pk=pk)
        phones = Telefon.objects.get(pk=umowa.phones.id)
        phones.dokument = False
        phones.save()
        umowa.delete()

        return redirect('umowa_komisowa')


@method_decorator(login_required, name='dispatch')
class UmowaIdView(View):
    def get(self, request, pk):
        umowa = UmowaKomisowaNew.objects.get(phones=pk)
        ctx = {'umowa': umowa}
        return render(request, 'umowa_id.html', ctx)


@method_decorator(login_required, name='dispatch')
class FakturaZakupuView(View):
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
                telefon.save()
                faktura.save()

            return HttpResponseRedirect('/checking_invoice/')
        else:
            print('Nie jest valid')
            return HttpResponseRedirect('/lista_faktur/')


@method_decorator(login_required, name='dispatch')
class CheckingInvoiceView(View):
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
class FakturaIdView(View):
    def get(self, request, pk):
        umowa = FakturaZakupu.objects.get(telefon=pk)
        ctx = {'umowa': umowa}
        return render(request, 'faktura_id.html', ctx)


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


@method_decorator(login_required, name='dispatch')
class TelefonCreateView(View):
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
                                   pracownik_zak=pracownik)

            return HttpResponseRedirect('/telefony_magazyn/')
        else:
            print('Nie jest valid')
            return HttpResponseRedirect('/')


@method_decorator(login_required, name='dispatch')
class ListaUmowView(View):
    def get(self, request):
        umowy = UmowaKomisowaNew.objects.all().order_by('-id')
        telefon = Telefon.objects.all().last()

        page = request.GET.get('page')
        paginator = Paginator(umowy, page_records)
        umowy_pagi = paginator.get_page(page)
        ctx = {'umowy': umowy_pagi}
        return render(request, 'lista_umow.html', ctx)

    def post(self, request):
        szukaj = request.POST.get('szukaj')

        umowa = UmowaKomisowaNew.objects.filter(
            Q(number__icontains=szukaj) | Q(komitent__icontains=szukaj)
            | Q(phones__nazwa__icontains=szukaj)
            | Q(phones__marka__nazwa__icontains=szukaj)
            | Q(phones__imei__icontains=szukaj))

        # faktury = FakturaZakupu.objects.filter(telefon__in=telefony)?
        # umowy = UmowaKomisowaNew.objects.filter(phones__in=telefony)
        ctx = {'umowy': umowa}
        return TemplateResponse(request, "lista_umow.html", ctx)


@method_decorator(login_required, name='dispatch')
class ListaFakturView(View):
    def get(self, request):
        faktury = FakturaZakupu.objects.all().order_by('-id')
        page = request.GET.get('page')
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
        page = request.GET.get('page')
        paginator = Paginator(faktury, page_records)
        faktury_pagi = paginator.get_page(page)
        ctx = {'faktury': faktury_pagi}
        return render(request, 'lista_faktur.html', ctx)


@method_decorator(login_required, name='dispatch')
class EdycjaFakturyView(UpdateView):
    model = FakturaZakupu
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/lista_faktur/')


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
class WystawTelefonView(UpdateView):
    model = Telefon
    fields = ['kategoria', 'stan', 'cena_sprzed', 'zdjecia']
    template_name_suffix = ('_update_form')
    success_url = ('/')


@method_decorator(login_required, name='dispatch')
class SzczegolyTelefonuView(UpdateView):
    model = Telefon
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/')


@method_decorator(login_required, name='dispatch')
class DodajUslugaView(CreateView):
    model = Usluga
    fields = '__all__'
    success_url = reverse_lazy("lista_uslug")


@method_decorator(login_required, name='dispatch')
class EdycjaUslugiView(UpdateView):
    model = Usluga
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/lista_uslug/')


@method_decorator(login_required, name='dispatch')
class ListaUslugView(View):
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
class DodajPremiaJobView(View):
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
class DodajInnePraceView(View):
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
class DashboardView(View):
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

        for pracownik in pracownicy:
            pracownik.licznik(uslugi)

        ctx = {
            'sklep': sklep_instacja,
            'uslugi': uslugi,
            'pracownicy': pracownicy,
            'miesiac': miesiac,
            'rok': rok,
            'typ': typ_uslugi
        }
        return TemplateResponse(request, "dashboard_sklepow.html", ctx)


@method_decorator(login_required, name='dispatch')
class TwojePremieJobView(View):
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
            'premia': premia_result,
            'zysk_netto': zysk_netto
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
            'premia': premia_result,
            'zysk_netto': zysk_netto
        }
        return TemplateResponse(request, "szczegoly_serwisow_serwisanta.html",ctx)

@method_decorator(login_required, name='dispatch')
class DodajAkcesoriaView(View):
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
class EdycjaPremiaJobView(UpdateView):
    model = PremiaJob
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/dashboard_sklepow/')

@method_decorator(login_required, name='dispatch')
class SzczegolySerwisySerwisantaView(View):
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
            'premia': premia_result,
            'zysk_netto': zysk_netto
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
            'premia': premia_result,
            'zysk_netto': zysk_netto
        }
        return TemplateResponse(request, "szczegoly_serwisow_serwisanta.html",ctx)
    # def get(self, request,pk,rok,miesiac):

    #     pracownik = MyUser.objects.get(pk=pk)
    #     miesiac=miesiac
    #     rok=rok
    #     data = MIESIACE[miesiac - 1][1]
    #     uslugi = PremiaJob.objects.filter(
    #         data__year=rok,
    #         data__month=miesiac).filter(pracownik=pracownik).order_by('-id')

    #     zysk = []
    #     premia = []
    #     for el in uslugi:
    #         if el.cena_klient is not None and el.koszt is not None:
    #             if el.cena_klient >= el.koszt:
    #                 zysk.append(el.cena_klient - el.koszt)
    #                 if el.usluga == 0:
    #                     premia.append(((el.cena_klient - el.koszt) *
    #                                (el.usluga.kwota)) / 100)
    #                     premia(print)
    #                 else:
    #                     premia.append(el.usluga.kwota)
    #                 print(premia)
    #             else:
    #                 premia.append(0)
    #     for el in premia:
    #         print(el)
    #     suma_zysk = sum(zysk)
    #     premia_result = sum(premia)
    #     zysk_netto = suma_zysk - premia_result

    #     ctx = {
    #         'uslugi': uslugi,
    #         'pracownik': pracownik,
    #         'miesiac': miesiac,
    #         'data': data,
    #         'rok': rok,
    #         'zysk': suma_zysk,
    #         'premia': premia_result,
    #         'zysk_netto': zysk_netto
    #     }
    #     return TemplateResponse(request, "szczegoly_serwisow_serwisanta.html",
    #                             ctx)
    

@method_decorator(login_required, name='dispatch')
class DodajSerwisView(View):
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
                                       imie_nazwisko=imei)

            return HttpResponseRedirect('/lista_serwisow/')
        else:
            print('Nie jest valid')
            return HttpResponseRedirect('/')


@method_decorator(login_required, name='dispatch')
class ListaSerwisowMagazynView(View):
    def get(self, request):
        serwisy = DodajSerwis.objects.filter(naprawa=True).order_by('-id')
        # serwisy = DodajSerwis.objects.all().order_by('-id')
        page = request.GET.get('page')
        paginator = Paginator(serwisy, page_records)
        serwisy_pagi = paginator.get_page(page)
        ctx = {'serwisy': serwisy_pagi}
        return render(request, 'serwisy.html', ctx)
    
    def post(self, request):
        szukaj = request.POST.get('szukaj')

        serwisy_dostepne = DodajSerwis.objects.filter(archiwum=False)
        serwisy = serwisy_dostepne.filter(Q(id__icontains=szukaj) |
            Q(marka__nazwa__icontains=szukaj) | Q(model__icontains=szukaj)
            | Q(imei__icontains=szukaj))
        page = request.GET.get('page')
        paginator = Paginator(serwisy, page_records)
        serwisy_pagi = paginator.get_page(page)
        ctx = {'serwisy': serwisy_pagi}
        return render(request, 'serwisy.html', ctx)
        
    
    

@method_decorator(login_required, name='dispatch')
class ListaSerwisowGotowychMagazynView(View):
    def get(self, request):
        serwisy = DodajSerwis.objects.filter(status="4").order_by('-id')
        ctx = {'serwisy': serwisy}
        return render(request, 'serwisy_gotowe.html', ctx)
    
    def post(self, request):
        szukaj = request.POST.get('szukaj')

        serwisy_dostepne = DodajSerwis.objects.filter(archiwum=False).filter(status=4)
        serwisy = serwisy_dostepne.filter(Q(id__icontains=szukaj) |
            Q(marka__nazwa__icontains=szukaj) | Q(model__icontains=szukaj)
            | Q(imei__icontains=szukaj))
        
        ctx = {'serwisy': serwisy}
        return TemplateResponse(request, 'serwisy_gotowe.html', ctx)


@method_decorator(login_required, name='dispatch')
class SzczegolySerwisuView(UpdateView):
    model = DodajSerwis
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/lista_serwisow/')


@method_decorator(login_required, name='dispatch')
class GotowySerwisView(View):
    def get(self, request, pk):
        serwis = DodajSerwis.objects.get(pk=pk)
        saldo = saldo_sms()
        ctx = {'serwis': serwis, 'saldo': saldo}
        return render(request, 'checking_service.html', ctx)


@method_decorator(login_required, name='dispatch')
class ServiceReadyView(View):
    def get(self, request, pk):
        service = DodajSerwis.objects.get(pk=pk)
        cena_zgoda = request.GET['cena']
        koszt = request.GET['koszt']
        info = request.GET['info']
        serwis_wlasny = request.GET['serwis_wlasny']
        premia = PremiaJob.objects.filter()
        # print(serwis_wlasny)
        if serwis_wlasny == "1":
            usluga = Usluga.objects.filter(czesci=True)
            premia = PremiaJob.objects.filter(usluga__in=usluga).last()
            if premia:
                if premia.check != service.id:
                    service.serwisant = request.user
                    service.cena_zgoda = cena_zgoda
                    service.koszt = koszt
                    service.info = info
                    service.status = "4"
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

                    # send(service.numer_telefonu, message)
                    return HttpResponseRedirect('/lista_serwisow/')
                else:
                    return HttpResponseRedirect('/lista_serwisow/')

            else:
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
                    # send(service.numer_telefonu, message)
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
class WydajSerwisView(View):
    def get(self, request, pk):
        serwis = DodajSerwis.objects.get(pk=pk)
        ctx = {'serwis': serwis}
        return render(request, 'checking2_service.html', ctx)

    def post(self, request, pk):
        service_id = request.POST['serwis_id']
        cena = request.POST['cena']
        premia=PremiaJob.objects.get(check=service_id)
        service = DodajSerwis.objects.get(pk=service_id)
        if cena!=service.cena_zgoda:
            premia.cena_klient=cena
            premia.save()
            service.cena_zgoda = cena
        service.status = "5"
        service.data_wydania = datetime.now()
        service.archiwum = True

        service.save()
        

        return redirect('/archiwum_serwisow/')


# @method_decorator(login_required, name='dispatch')
# class ServiceSentView(View):
#     pass


#     def post(self, request):
#         service_id = request.POST['serwis_id']
#         service = DodajSerwis.objects.get(pk=service_id)
#         service.status = "5"
#         service.data_wydania = datetime.now()
#         service.archiwum = True

#         service.save()

#         return redirect('/archiwum_serwisow/')


@method_decorator(login_required, name='dispatch')
class ArchiwumSerwisView(View):
    def get(self, request):
        serwisy = DodajSerwis.objects.filter(archiwum=True).order_by('-id')
        page = request.GET.get('page')
        paginator = Paginator(serwisy, page_records)
        serwisy_pagi = paginator.get_page(page)
        ctx = {'serwisy': serwisy_pagi}
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
class ReklamacjaSerwisView(View):
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


@method_decorator(login_required, name='dispatch')
class DodajTypView(CreateView):
    model = Typ
    fields = '__all__'
    success_url = reverse_lazy("lista_typ")


@method_decorator(login_required, name='dispatch')
class TypView(CreateView):
    def get(self, request):
        typ = Typ.objects.all()
        ctx = {"typ": typ}
        return render(request, 'lista_typ.html', ctx)


@method_decorator(login_required, name='dispatch')
class CzesciCreateView(View):
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
                czesc.foto.add(foto)
                czesc.save()

            return HttpResponseRedirect('/lista_czesci/')
        else:
            print('Nie jest valid')
            return HttpResponseRedirect('')


@method_decorator(login_required, name='dispatch')
class TypView(View):
    def get(self, request):
        typ = Typ.objects.all()
        ctx = {"typ": typ}
        return render(request, 'lista_typ.html', ctx)


@method_decorator(login_required, name='dispatch')
class ListaCzesciView(View):
    def get(self, request):
        czesc = Czesc.objects.all()
        page = request.GET.get('page')
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
        paginator = Paginator(czesc, page_records)
        czesc_pagi = paginator.get_page(page)
        ctx = {"czesc": czesc_pagi, 'paginator': paginator}
        return render(request, 'lista_czesci.html', ctx)


@method_decorator(login_required, name='dispatch')
class AddMoreItemsView(View):
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
class AddMoreItemsSimiliarView(View):
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
class RemoveMoreItemsView(View):
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
class SzczegolyCzesciView(UpdateView):
    model = Czesc
    fields = '__all__'
    template_name_suffix = ('_update_form')
    success_url = ('/lista_czesci/')


@method_decorator(login_required, name='dispatch')
class UzyjCzesciView(View):
    def post(self, request):
        form = CenaKlientForm()
        czesci_lista = request.POST.getlist('checks')
        # print(czesci_lista)

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
            'serwisy': serwisy,
            'saldo': saldo,
            'czesci_lista': czesci_lista
        }
        return render(request, 'wydaj_serwis_czesci.html', ctx)


@method_decorator(login_required, name='dispatch')
class WydajSerwisCzesciView(View):
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
            return HttpResponseRedirect('/lista_serwisow_gotowych/')

        return HttpResponseRedirect('/RETURNERRORS/')

@method_decorator(login_required, name='dispatch')
class WydajSerwisCzesci2View(View):
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
            return HttpResponseRedirect('/lista_serwisow_gotowych/')

        return HttpResponseRedirect('/RETURNERRORS/')


@method_decorator(login_required, name='dispatch')
class GetServiceForItems(View):
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
class UzyjCzesciSerwisView(View):
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
