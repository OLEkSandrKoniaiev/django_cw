# Generated by Django 5.1.1 on 2024-09-11 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0009_alter_carmodel_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carmodel',
            name='currency',
        ),
    ]
