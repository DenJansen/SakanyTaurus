# Generated by Django 3.0.3 on 2020-03-24 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sakanyapp', '0004_routestep_distance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routestep',
            name='distance',
        ),
    ]
