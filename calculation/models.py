from django.db import models
from django.template.defaultfilters import default
from restaurant.models import Restaurant
# Create your models here. 

class Result(models.Model):
    rest = models.ForeignKey('restaurant.Restaurant',on_delete=models.CASCADE)
    day = models.IntegerField()
    date = models.DateField()