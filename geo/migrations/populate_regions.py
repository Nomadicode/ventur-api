import json
from django.db import migrations, models, transaction

from geo.models import Country, Region


def populate_regions(apps, schema_editor):
    with open('core_data/regions.json') as f:
        data = json.load(f)

    for country_dict in data:
        try:
            country = Country.objects.get(alpha_2_code=country_dict['alpha_2_code'])
        except Country.DoesNotExist:
            print(country_dict['name'], country_dict['alpha_2_code'])
            continue

        for region in country_dict['regions']:
            region['country'] = country
            try:
                new_region = Region(**region)
                new_region.save()
            except Exception as e:
                print(region, e)
                continue


class Migration(migrations.Migration):
    dependencies = [
        ('geo', 'populate_countries')
    ]

    operations = [
        migrations.RunPython(populate_regions)
    ]
