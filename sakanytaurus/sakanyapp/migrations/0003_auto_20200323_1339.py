# Generated by Django 3.0.3 on 2020-03-23 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sakanyapp', '0002_auto_20200313_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routestep',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='sakanyapp.UserRoute'),
        ),
    ]
