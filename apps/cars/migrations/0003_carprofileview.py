# Generated by Django 5.1 on 2024-09-09 09:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_carmodel_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarProfileView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('car', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='car_profiles', to='cars.carmodel')),
            ],
            options={
                'db_table': 'car_profiles',
                'ordering': ('id',),
            },
        ),
    ]
