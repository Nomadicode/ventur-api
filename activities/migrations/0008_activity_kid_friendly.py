# Generated by Django 2.1.2 on 2019-09-03 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_auto_20190806_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='kid_friendly',
            field=models.BooleanField(default=False),
        ),
    ]
