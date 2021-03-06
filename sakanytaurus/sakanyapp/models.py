from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

# Create your models here.
class UserRoute(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 20)
    creation_dtg = models.DateTimeField(
        default = datetime.now
    )
    start_time = models.DateTimeField(
        blank = True,
        null = True
    )
    end_time = models.DateTimeField(
        blank = True,
        null = True
    )

    def start_dt (self):
        return self.start_time.strftime("%d %b %Y %H:%M") if self.start_time else ''

    def end_dt (self):
        return self.end_time.strftime("%d %b %Y %H:%M") if self.end_time else ''

    def __str__(self):
        return 'User: ' + str(self.creator) + ' | Route Name: ' + self.name + ' | Start: ' + self.start_dt() + ' | End: ' + self.end_dt()

class RouteStep(models.Model):
    route = models.ForeignKey(UserRoute, on_delete=models.CASCADE, related_name='steps')
    order_num = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    loc_name = models.CharField(max_length = 30)
    loc_rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    loc_address = models.TextField()
    loc_lat = models.FloatField()
    loc_lon = models.FloatField()
    open_time = models.DateTimeField(
        blank = True,
        null = True
    )
    close_time = models.DateTimeField(
        blank = True,
        null = True
    )
    arr_time = models.DateTimeField(
        blank = True,
        null = True
    )
    visited = models.BooleanField(default=False)
    distance = models.FloatField()
    newdistance = models.FloatField()
    unit = models.CharField(max_length = 20)
    stars = models.PositiveSmallIntegerField()
    halfstar = models.FloatField()
    review_count = models.PositiveSmallIntegerField()

    def __str__(self):
        return ' Route: ' + self.route.name + ' | Step: ' + str(self.order_num) + ' | Arrival Time: ' + str(self.arr_time) + ' | Visited: ' + str(self.visited)
