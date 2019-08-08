# Generated by Django 2.1.2 on 2019-08-04 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_auto_20190708_0500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='responded',
            new_name='resolved',
        ),
        migrations.AddField(
            model_name='report',
            name='upheld',
            field=models.BooleanField(default=False),
        ),
    ]