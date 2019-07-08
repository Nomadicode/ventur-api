import environ
from django.db import migrations

from django.contrib.sites.models import Site

def update_core_settings(apps, schema_editor):
    site = Site.objects.first()

    env = environ.Env()
    config = env('DJANGO_CONFIGURATION')

    if config == 'Local':
        site.domain = 'http://localhost:8000'
        site.name = 'Driftr Local'

    if config == 'Dev':
        site.domain = 'https://api-dev.driftr.app'
        site.name = 'Driftr Dev'

    if config == 'Prod':
        site.domain = 'https://api.driftr.app'
        site.name = 'Driftr'

    site.save()


class Migration(migrations.Migration):
    dependencies = [
        ('users', 'create_system_user')
    ]

    operations = [
        migrations.RunPython(update_core_settings)
    ]
