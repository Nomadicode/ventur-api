# Generated by Django 2.1.1 on 2018-09-30 01:52
import json
from django.db import migrations, models

from geo.models import Continent


def populate_continents(apps, schema_editor):
    with open('core_data/continents.json') as f:
        data = json.load(f)

    for continent in data:
        try:
            new_continent = Continent(**continent)
            new_continent.save()
        except Exception:
            print(continent)
            continue


class Migration(migrations.Migration):
    dependencies = [
        ('geo', '0001_initial')
    ]

    operations = [
        migrations.RunPython(populate_continents)
    ]
