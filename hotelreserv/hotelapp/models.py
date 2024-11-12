from django.db import models

# Create your models here.

class Room(models.Model):
    number = models.IntegerField(unique=True)
    floor = models.IntegerField()
    bedrooms = models.IntegerField()
    is_available = models.BooleanField(default=True)

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
