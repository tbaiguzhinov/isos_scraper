from django.contrib import admin

from isos.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']