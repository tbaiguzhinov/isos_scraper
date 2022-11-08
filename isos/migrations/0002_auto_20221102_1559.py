# Generated by Django 3.2.7 on 2022-11-02 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isos', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'Countries'},
        ),
        migrations.AddField(
            model_name='country',
            name='isos_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='ISOS number'),
        ),
    ]
