# Generated by Django 3.0.4 on 2020-04-03 06:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sakanyapp', '0006_auto_20200402_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='userroute',
            name='creation_dtg',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
