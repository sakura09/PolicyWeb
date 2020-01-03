from django.db import models

# Create your models here.
from django.db import models

class Talent(models.Model):
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    addr = models.CharField(max_length=1001)

class Policy(models.Model):
    standard = models.CharField(max_length=200)
    award = models.CharField(max_length=400)