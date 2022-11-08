from django.shortcuts import render

from isos.models import Country


def get_countries(request):
    countries = Country.objects.filter(isos_code__gt=0).order_by('name')
    return render(request, template_name='index.html', context={'countries': countries})


def get_country(request, id):
    country = Country.objects.get(id=id)
    return render(request, template_name='country.html', context={'country': country})
