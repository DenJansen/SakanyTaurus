# Generated by Django 3.0.4 on 2020-03-13 17:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route', models.CharField(max_length=20)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RouteStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)])),
                ('loc_name', models.CharField(max_length=30)),
                ('loc_rating', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('loc_address', models.TextField()),
                ('loc_lat', models.FloatField()),
                ('loc_lon', models.FloatField()),
                ('open_time', models.DateTimeField(blank=True, null=True)),
                ('close_time', models.DateTimeField(blank=True, null=True)),
                ('arr_time', models.DateTimeField(blank=True, null=True)),
                ('visited', models.BooleanField(default=False)),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sakanyapp.UserRoute')),
            ],
        ),
    ]
