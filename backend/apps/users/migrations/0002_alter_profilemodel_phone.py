# Generated by Django 5.1 on 2024-09-09 20:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilemodel',
            name='phone',
            field=models.CharField(max_length=13, validators=[django.core.validators.RegexValidator('^\\+380(39|50|63|66|67|68|73|91|92|93|94|95|96|97|98|99)\\d{7}$', ['Phone number must start with +380', 'Phone number must contain a valid operator code (39, 50, 63, 66, 67, 68, 73, 91, 92, 93, 94, 95, 96, 97, 98, 99)', 'Phone number must contain exactly 7 digits after the operator code'])]),
        ),
    ]
