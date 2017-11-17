from django.db import models

# Create your models here.
from django.db import models
from django.db import models

# the following lines added:q
import datetime
from django.utils import timezone

class OptimalWeather(models.Model):
    min_temp = models.FloatField()
    max_temp = models.FloatField()
    pressure = models.FloatField()
    skycover = models.FloatField()
    water_avail = models.FloatField()
    humiditiy = models.FloatField()
    wind_speed = models.FloatField()
    wind_degree = models.FloatField()
    rain_forecast =  models.FloatField()

    def __str__(self):
        return self.name

'''class Question(models.Model):
   question_text = models.CharField(max_length=200)
   pub_date = models.DateTimeField('date published')

   def __str__(self):
       return self.question_text

   def was_published_recently(self):
       now = timezone.now()
       return now - datetime.timedelta(days=1) <= self.pub_date <= now

   was_published_recently.admin_order_field = 'pub_date'
   was_published_recently.boolean = True
   was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
   question = models.ForeignKey(Question)
   choice_test = models.CharField(max_length=200)
   votes = models.IntegerField(default=0)

   def __str__(self):
       return self.choice_test
'''