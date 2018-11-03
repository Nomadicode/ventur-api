# Generated by Django 2.1.1 on 2018-09-30 01:52
import json
from django.db import migrations, models

from geo.models import Country, Continent


def populate_countries(apps, schema_editor):
    with open('core_data/countries.json') as f:
        data = json.load(f)

    for country in data:
        continent = Continent.objects.get(alpha_2_code=country['continent'])
        country['continent'] = continent
        
        try:
            new_country = Country(**country)
            new_country.save()
        except Exception:
            print(country)
            continue


class Migration(migrations.Migration):
    dependencies = [
        ('geo', 'populate_continents')
    ]

    operations = [
        migrations.RunPython(populate_countries)
    ]
