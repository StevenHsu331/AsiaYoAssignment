# Generated by Django 5.0.6 on 2024-09-28 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('address_city', models.CharField(max_length=128)),
                ('address_district', models.CharField(max_length=128)),
                ('address_street', models.CharField(max_length=128)),
                ('currency', models.CharField(max_length=8)),
            ],
        ),
    ]
