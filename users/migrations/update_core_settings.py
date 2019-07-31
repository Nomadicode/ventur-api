import environ
from django.db import migrations

from django.contrib.sites.models import Site

def update_core_settings(apps, schema_editor):
    env = environ.Env()
    config = env('DJANGO_CONFIGURATION')

    domain = 'http://localhost:8000'
    name = 'Ventür Local'

    if config == 'Dev':
        domain = 'https://api-dev.ventur.app'
        name = 'Ventür Dev'

    if config == 'Prod':
        domain = 'https://api.ventur.app'
        name = 'Ventür'

    Site.objects.create(domain=domain, name=name)


class Migration(migrations.Migration):
    dependencies = [
        ('users', 'create_system_user')
    ]

    operations = [
        migrations.RunPython(update_core_settings)
    ]
