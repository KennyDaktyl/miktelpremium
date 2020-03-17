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
        ctx = {"czesc": czesc_pagi}
        return render(request, 'lista_czesci.html', ctx)


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
        print(czesci_lista)

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
        print(marka)
        usluga = Usluga.objects.filter(czesci=True)
        serwisy = DodajSerwis.objects.filter(
            usluga__in=usluga).filter(naprawa=True).filter(marka=marka)
        ctx = {'form': form, 'query_list': query_list, 'total': total, 'marka': marka,
               'serwisy': serwisy, 'saldo': saldo, 'czesci_lista': czesci_lista}
        return render(request, 'wydaj_serwis_czesci.html', ctx)


@method_decorator(login_required, name='dispatch')
class WydajSerwisCzesciView(View):
    def post(self, request):
        czesci_lista = request.POST.getlist('checks')
        koszt = request.POST.get('koszt')
        serwis_id = request.POST.get('serwis_id')
        cena_zgoda = request.POST.get('cena_klient')

        total_koszt = []
        query_list = []

        usluga = Usluga.objects.filter(czesci=True)
        premia = PremiaJob.objects.filter(usluga__in=usluga).last()
        print(premia.check)

        if serwis_id != "":
            serwis = DodajSerwis.objects.get(pk=serwis_id)
            if not premia:
                print("not")
                premia = PremiaJob.objects.create(check=serwis_id, sklep=request.user.sklep_dzisiaj, pracownik=request.user,
                                                  usluga=serwis.usluga, model=serwis.model, cena_klient=cena_zgoda, koszt=koszt)
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
                zysk = int(cena_zgoda)-koszt

                subject = "Wykonano serwis z wielu czesci w {} przez {}".format(
                    premia.sklep, premia.pracownik)
                text = "{} wykonał {} w {} za {} zysk {}".format(premia.pracownik,
                                                                 premia.usluga,
                                                                 premia.model, premia.cena_klient, zysk
                                                                 )
                send_email(subject, text)

            else:
                if int(premia.check) != int(serwis_id):
                    print("jestem tutuaj")
                    print(premia.check)
                    print(serwis_id)
                    premia = PremiaJob.objects.create(check=serwis_id, sklep=request.user.sklep_dzisiaj, pracownik=request.user,
                                                      usluga=serwis.usluga, model=serwis.model, cena_klient=cena_zgoda, koszt=koszt)

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

                    zysk = int(cena_zgoda)-koszt

                    subject = "Wykonano serwis z wielu czesci w {} przez {}".format(
                        premia.sklep, premia.pracownik)
                    text = "{} wykonał {} w {} za {} zysk {}".format(premia.pracownik,
                                                                     premia.usluga,
                                                                     premia.model, premia.cena_klient, zysk
                                                                     )
                    send_email(subject, text)
            return HttpResponseRedirect('/lista_serwisow/')

        return HttpResponseRedirect('/RETURNERRORS/')
