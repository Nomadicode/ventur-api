# Generated by Django 2.1.2 on 2019-07-17 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_auto_20190717_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
