# Generated by Django 2.1.2 on 2019-08-06 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0006_auto_20190717_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='media',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
