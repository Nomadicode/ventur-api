# Generated by Django 2.1.2 on 2019-02-10 03:15

from django.db import migrations
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='schedule',
        ),
        migrations.AddField(
            model_name='activity',
            name='recurrence',
            field=recurrence.fields.RecurrenceField(blank=True, null=True),
        ),
    ]