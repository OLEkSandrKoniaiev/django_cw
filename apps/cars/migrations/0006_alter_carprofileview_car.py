# Generated by Django 5.1 on 2024-09-09 10:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0005_carmodel_edit_attempts_carprofileview_body_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carprofileview',
            name='car',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='car_profiles', to='cars.carmodel'),
        ),
    ]
