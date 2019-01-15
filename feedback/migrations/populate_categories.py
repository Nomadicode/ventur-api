# Generated by Django 2.1.1 on 2018-09-30 01:52
from django.db import migrations

from feedback.models import FeedbackCategory


def populate_categories(apps, schema_editor):
    data = [
        {
            "name": "Bug Report"
        }, {
            "name": "Feature Request"
        }, {
            "name": "Information"
        }, {
            "name": "Other"
        }
    ]

    for category in data:
        try:
            new_category = FeedbackCategory(**category)
            new_category.save()
        except Exception:
            print(category)
            continue


class Migration(migrations.Migration):
    dependencies = [
        ('feedback', '0001_initial')
    ]

    operations = [
        migrations.RunPython(populate_categories)
    ]