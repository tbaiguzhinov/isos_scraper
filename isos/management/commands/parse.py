import requests
import datetime
import os

from html2text import HTML2Text
from xlsxwriter import Workbook

from django.core.management import BaseCommand

from isos.management.commands.parsers import (get_content, get_cultural_tips,
                                              get_getting_around,
                                              get_getting_there, get_medical,
                                              get_phone_and_power,
                                              get_summary_and_advice,
                                              get_risk_ratings)
from isos.management.commands.upload_file import upload_file
from isos.models import Country

links = {
    'Summary': 'sec',
    'Personal Risk': 'persrisk',
    'Country Stability': 'ctrystability',
    'Getting There': 'there',
    'Getting Around': 'around',
    'Language and Money': 'languageandmoney',
    'Cultural Tips': 'tips',
    'Phone and Power': 'voltage',
    'Geography and Weather': 'weather',
    'Calendar': 'cal',
    'Before you go': 'precautions',
}


def get_page(content_tag, country_code):
    response = requests.get(
        'https://www.internationalsos.com/MasterPortal/default.aspx',
        params={
            'membnum': '14AYSA000043',
            'content': content_tag,
            'countryid': country_code,
        }
    )
    if response.ok:
        return response.text
    print(f'--- unable to load {content_tag} for {country_code}')


def gather_info():
    countries = Country.objects.all()
    for country in countries:
        country_code = country.isos_code

        landing_page = get_page('landing', country_code)

        summary = get_page(links['Summary'], country_code)
        personal_risk = get_page(links['Personal Risk'], country_code)
        country_stability = get_page(
            links['Country Stability'], country_code)
        getting_there = get_page(links['Getting There'], country_code)
        getting_around = get_page(links['Getting Around'], country_code)
        language_and_money = get_page(
            links['Language and Money'], country_code)
        cultural_tips = get_page(links['Cultural Tips'], country_code)
        phone_and_power = get_page(links['Phone and Power'], country_code)
        geography_and_weather = get_page(
            links['Geography and Weather'], country_code)
        calendar = get_page(links['Calendar'], country_code)
        medical = get_page(links['Before you go'], country_code)

        if summary:
            travel_risk_summary, standing_travel_advice = get_summary_and_advice(
                summary)
            country.travel_risk_summary = travel_risk_summary
            country.standing_travel_advice = standing_travel_advice

        if personal_risk:
            country.personal_risk = get_content(personal_risk, 'CRIME')

        if country_stability:
            country.country_stability = get_content(
                country_stability, 'POLITICAL SITUATION')

        if getting_there:
            country.getting_there = get_getting_there(getting_there)

        if getting_around:
            country.getting_around = get_getting_around(getting_around)

        if language_and_money and phone_and_power:
            language_money = get_content(language_and_money, 'LANGUAGE')
            phone_power = get_phone_and_power(phone_and_power)
            country.practicalities = language_money + phone_power

        if geography_and_weather:
            country.geography_and_weather = get_content(
                geography_and_weather, 'Climate')

        if cultural_tips and calendar:
            try:
                calendar = get_content(calendar, '2023')
            except AttributeError:
                calendar = ''
                print(f'Unable to load calendar for {country}')
            cultural_tips = get_cultural_tips(cultural_tips)
            country.cultural_tips = cultural_tips + calendar

        if medical:
            advice, vaccinations, diseases = get_medical(medical)
            country.medical_advice = advice
            country.vaccinations = vaccinations
            country.diseases = diseases

        if landing_page:
            medical_risk_rating, travel_security_risk_rating = get_risk_ratings(
                landing_page)
            country.medical_risk_rating = medical_risk_rating
            country.security_risk_rating = travel_security_risk_rating

        country.save()


def create_excel(file_dir, file_name):
    def convert_html(text):
        h = HTML2Text()
        h.body_width = 0
        return h.handle(text)

    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    wb = Workbook(os.path.join(file_dir, file_name))

    categories_names = [
        'Medical Risk',
        'ISOS Travel Security Risk Rating',
        'ISOS Risk summary',
        'ISOS Standing Travel Advice',
        'ISOS Travel Security Risks',
        'ISOS Political situation',
        'ISOS Getting there',
        'ISOS In-country travel',
        'ISOS Practicalities',
        'ISOS Background Brief',
        'ISOS Diplomatic representation',
        'ISOS Medical Advice',
        'ISOS Vaccination',
        'ISOS Diseases',
        'ISOS Last Update',
        # 'Library Workflow',
    ]
    short_names = [
        'External Ref ID',
        'Name',
        'Description',
        'MEDRISK',
        'ISOSTRAVEL',
        'RISKSUMMAR',
        'STANDINGTR',
        'TRAVELSECU',
        'POLITICALS',
        'GETTINGTHE',
        'IN-COUNTRY',
        'PRACTICALI',
        'BACKGROUND',
        'DIPLOMATIC',
        'ISOSMEDICA',
        'ISOSVACCIN',
        'ISOSDISEAS',
        'ISOSLASTUP',
        # 'Country Travel',
    ]
    sheet1 = wb.add_worksheet('Country Staff')
    wb.add_format({'num_format': 'dd.mm.yyyy'})

    sheet1.write(0, 0, 'Object Type ID')
    sheet1.write(1, 0, 'd3c9c53d-d7b4-4ae7-ab62-2b94e2e17c0d')

    column = 3
    for category in categories_names:
        sheet1.write(2, column, category)
        column += 1

    column = 0
    for name in short_names:
        sheet1.write(3, column, name)
        column += 1

    countries = Country.objects.all()

    row = 4
    for country in countries.iterator():
        sheet1.write(row, 0, country.name + " Staff")
        sheet1.write(row, 1, country.name)
        sheet1.write(row, 3, country.medical_risk_rating)
        sheet1.write(row, 4, country.security_risk_rating)
        sheet1.write(row, 5, convert_html(country.travel_risk_summary))
        sheet1.write(row, 6, convert_html(country.standing_travel_advice))
        sheet1.write(row, 7, convert_html(country.personal_risk))
        sheet1.write(row, 8, convert_html(country.country_stability))
        sheet1.write(row, 9, convert_html(country.getting_there))
        sheet1.write(row, 10, convert_html(country.getting_around))
        sheet1.write(row, 11, convert_html(country.practicalities))
        sheet1.write(row, 12, convert_html(country.geography_and_weather))
        sheet1.write(row, 13, convert_html(country.cultural_tips))
        sheet1.write(row, 14, convert_html(country.medical_advice))
        sheet1.write(row, 15, convert_html(country.vaccinations))
        sheet1.write(row, 16, convert_html(country.diseases))
        sheet1.write_datetime(row, 17, datetime.date.today())
        row += 1

    wb.close()


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(datetime.date.today(), ' parsing in progress:')
        file_dir = 'import'
        file_name = 'import.xlsx'
        gather_info()
        create_excel(file_dir, file_name)
        upload_file(file_dir, file_name)