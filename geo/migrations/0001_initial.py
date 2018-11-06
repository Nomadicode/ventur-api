# Generated by Django 2.1.2 on 2018-10-21 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('latitude', models.DecimalField(decimal_places=13, max_digits=16)),
                ('longitude', models.DecimalField(decimal_places=13, max_digits=16)),
            ],
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('alpha_2_code', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('alpha_2_code', models.CharField(max_length=2)),
                ('alpha_3_code', models.CharField(max_length=3)),
                ('continent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='countries', to='geo.Continent')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('alpha_2_code', models.CharField(max_length=5)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regions', to='geo.Country')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='geo.Region'),
        ),
    ]