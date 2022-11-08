from django.db import models


class Country(models.Model):
    name = models.CharField(
        'Country name',
        max_length=100,
    )
    isos_code = models.IntegerField(
        'ISOS number',
        blank=True,
        null=True,
    )
    
    ratings = [
        ('EXTREME', 'EXTREME'),
        ('HIGH', 'HIGH'),
        ('MEDIUM', 'MEDIUM'),
        ('LOW', 'LOW'),
        ('INSIGNIFICANT', 'INSIGNIFICANT'),
    ]
    
    medical_risk_rating = models.CharField(
        'Medical Risk Rating',
        max_length=100,
        choices=ratings,
    )
    
    security_risk_rating = models.CharField(
        'Travel Security Risk Rating',
        max_length=100,
        choices=ratings,
    )
    
    travel_risk_summary = models.TextField(
        'Travel Risk Summary',
    )
    standing_travel_advice = models.TextField(
        'Standing Travel Advice',
    )
    personal_risk = models.TextField(
        'Personal Risk',
    )
    country_stability = models.TextField(
        'Country Stability',
    )
    getting_there = models.TextField(
        'Getting There',
    )
    getting_around = models.TextField(
        'Getting Around',
    )
    cultural_tips = models.TextField(
        'Cultural Tips',
    )
    practicalities = models.TextField(
        'Practicalities',
    )
    geography_and_weather = models.TextField(
        'Geography and Weather',
    )
    medical = models.TextField(
        'Before you go',
    )
    medical_advice = models.TextField(
        'Before you go',
    )
    vaccinations = models.TextField(
        'Vaccinations',
    )
    diseases = models.TextField(
        'Diseases',
    )

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name
