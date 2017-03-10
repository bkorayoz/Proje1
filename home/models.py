from django.db import models

# Create your models here.

class Users(models.Model):
    userName = models.CharField(max_length =30)
    userMail = models.EmailField(default = 'email@email.com')

    def __str__(self):
        return self.userName
    def __str__(self):
        return self.userMail