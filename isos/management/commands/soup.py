from django.core.management import BaseCommand

from isos.management.commands.parsers import (get_content, get_cultural_tips,
                                              get_getting_around,
                                              get_getting_there, get_medical,
                                              get_phone_and_power)
from isos.models import Country


class Command(BaseCommand):

    def handle(self, *args, **options):
        countries = Country.objects.filter(isos_code__gt=0)
        for country in countries:
            print('Loading', country, country.id)
            advice, vaccinations, diseases = get_medical(country.medical)
            country.medical_advice = advice
            country.vaccinations = vaccinations
            country.diseases = diseases
            country.save()

            break
