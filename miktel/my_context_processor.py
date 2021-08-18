from miktel.models import Sklep, MyUser


def sklepy(request):
    sklepy = Sklep.objects.all().order_by("nazwa")
    ctx = {
        "sklepy": sklepy,
        "version": "1.0",
    }
    return ctx


# from django import template

# register = template.Library()

# @register.simple_tag(takes_context=True)
# def query_transform(context, **kwargs):
#     query = context['request'].GET.copy()
#     for k, v in kwargs.items():
#         query[k] = v
#     return query.urlencode()
