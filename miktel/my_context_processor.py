from miktel.models import Sklep, MyUser


def sklepy(request):
    sklepy = Sklep.objects.all().order_by("nazwa")
    ctx = {
        "sklepy": sklepy,
        "version": "1.0",
    }
    return ctx


# def pracownicy(request):
#     pracownicy = MyUser.objects.all().order_by("username")
#     ctx = {
#         "pracownicy": pracownicy,
#         "version": "1.0",
#     }
#     return ctx
