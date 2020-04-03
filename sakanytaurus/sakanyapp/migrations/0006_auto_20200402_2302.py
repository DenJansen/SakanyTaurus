# Generated by Django 3.0.4 on 2020-04-03 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sakanyapp', '0005_remove_routestep_distance'),
    ]

    operations = [
        migrations.AddField(
            model_name='routestep',
            name='distance',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='routestep',
            name='halfstar',
            field=models.FloatField(default=0.5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='routestep',
            name='newdistance',
            field=models.FloatField(default=234),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='routestep',
            name='review_count',
            field=models.PositiveSmallIntegerField(default=234),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='routestep',
            name='stars',
            field=models.PositiveSmallIntegerField(default=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='routestep',
            name='unit',
            field=models.CharField(default='ft', max_length=20),
            preserve_default=False,
        ),
    ]