# Generated by Django 2.1.2 on 2019-09-09 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0009_auto_20190909_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='minimum_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
