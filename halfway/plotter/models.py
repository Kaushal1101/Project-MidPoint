from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here

class User(AbstractUser):
    pass

class Place(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    lat = models.FloatField(default=1.2838)
    lng = models.FloatField(default=103.8591)