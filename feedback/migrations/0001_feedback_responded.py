# Generated by Django 2.1.2 on 2019-07-08 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', 'populate_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='responded',
            field=models.BooleanField(default=False),
        ),
    ]
