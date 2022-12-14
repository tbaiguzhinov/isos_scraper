# Generated by Django 3.2.7 on 2022-11-07 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isos', '0008_auto_20221107_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='medical_risk_rating',
            field=models.CharField(choices=[('EXTREME', 'EXTREME'), ('HIGH', 'HIGH'), ('MEDIUM', 'MEDIUM'), ('LOW', 'LOW'), ('INSIGNIFICANT', 'INSIGNIFICANT')], default=('INSIGNIFICANT', 'INSIGNIFICANT'), max_length=100, verbose_name='Medical Risk Rating'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='country',
            name='security_risk_rating',
            field=models.CharField(choices=[('EXTREME', 'EXTREME'), ('HIGH', 'HIGH'), ('MEDIUM', 'MEDIUM'), ('LOW', 'LOW'), ('INSIGNIFICANT', 'INSIGNIFICANT')], default=('INSIGNIFICANT', 'INSIGNIFICANT'), max_length=100, verbose_name='Travel Security Risk Rating'),
            preserve_default=False,
        ),
    ]
