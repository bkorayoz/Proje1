from django.db import models
from _datetime import date

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    transportation = models.BooleanField(default=False)
    weatherSensetion = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    counter = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def deleteRest(self, deleteId):
        self.objects.filter(id=deleteId).delete()

    def updateStatus(self, newStatus, updateId):
        self.objects.get(id=updateId).update(status = newStatus)



