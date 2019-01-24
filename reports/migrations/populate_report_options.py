from django.db import migrations

from reports.models import ReportCategory


def populate_report_options(apps, schema_editor):
    data = [
        {
            "name": "Misleading or Scam",
            "detail": "This activity is misleading and/or a scam"
        }, {
            "name": "Spam",
            "detail": "This activity is spam"
        }, {
            "name": "Hate Speech",
            "detail": "This activity contains hate speech"
        }, {
            "name": "Violence",
            "detail": "This activity promotes or encourages violence"
        }, {
            "name": "Sexual Content",
            "detail": "This activity contains sexually explicit content"
        }, {
            "name": "Self Harm",
            "detail": "This activity encourages or states a desire to cause self harm"
        }, {
            "name": "Risky Behavior",
            "detail": "This activity is risky or possibly hazardous"
        }, {
            "name": "Harassment or threatening",
            "detail": "This activity is harassing, threatening, or encourages harassment or threats"
        }, {
            "name": "Illegal Behavior",
            "detail": "This activity encourages illegal behavior"
        }, {
            "name": "Other",
            "detail": "This activity violates the Terms of Service and/or promotes an unsafe or unwelcoming community"
        }
    ]

    for option in data:
        try:
            new_option = ReportCategory.objects.create(**option)
        except Exception:
            print(option)
            continue


class Migration(migrations.Migration):
    dependencies = [
        ('reports', '0001_initial')
    ]

    operations = [
        migrations.RunPython(populate_report_options)
    ]
