# Generated by Django 2.1.2 on 2019-01-24 18:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', 'populate_repeat_options'),
        ('preferences', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved', models.DateTimeField(auto_now_add=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_activities', to='activities.Activity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_activities', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='acceptedactivity',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accepted_activities', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rejectedactivity',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rejected_activities', to=settings.AUTH_USER_MODEL),
        ),
    ]