from django.db import models
from restaurant.models import Restaurant
# Create your models here.

class Users(models.Model):
    userName = models.CharField(max_length =30)
    userMail = models.EmailField(default = 'email@email.com')

    def __str__(self):
        return self.userName
    def __str__(self):
        return self.userMail
    
class Grade(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    grade = models.IntegerField()