# Generated by Django 3.2.7 on 2022-11-07 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('isos', '0004_auto_20221107_1033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='summary',
        ),
    ]
