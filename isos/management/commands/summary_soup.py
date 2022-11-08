from django.core.management import BaseCommand

from isos.management.commands.parsers import get_summary_and_advice
from isos.models import Country


class Command(BaseCommand):

    def handle(self, *args, **options):
        countries = Country.objects.filter(isos_code__gt=0)
        for country in countries:
            print('Loading', country, country.id)
            summary = country.summary
            travel_risk_summary, standing_travel_advice = get_summary_and_advice(summary)
            country.travel_risk_summary = travel_risk_summary
            country.standing_travel_advice = standing_travel_advice
            country.save()