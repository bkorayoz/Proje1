from django.db import models

# Create your models here.

class Users(models.Model):
    userName = models.CharField(max_length =30)

    def __str__(self):
        return self.userName