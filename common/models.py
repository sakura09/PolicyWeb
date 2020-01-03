from django.db import models

# Create your models here.
from django.db import models

class Policy(models.Model):
    #
    #policyName = models.CharField(max_length=10000)

    url = models.CharField(max_length=1000, null=True, blank=True)

    updateTime = models.DateTimeField(max_length=10000, null=True, blank=True)

    Name = models.CharField(max_length=10000)

    method = models.CharField(max_length=10000)

    type = models.CharField(max_length=10000)

    addr = models.CharField(max_length=10000)

    categoryContent = models.CharField(max_length=100000)

    num = models.IntegerField(max_length=1000, null=True, blank=True)


