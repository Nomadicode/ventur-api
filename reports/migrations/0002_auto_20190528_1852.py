# Generated by Django 2.1.2 on 2019-05-28 18:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_auto_20190122_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reported_activities', to=settings.AUTH_USER_MODEL),
        ),
    ]
