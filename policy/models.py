from django.db import models

# Create your models here.
from django.db.models import Sum


class talentType(models.Model):
    #typeName = models.CharField(max_length=200, null=False, primary_key=True)
    typeName = models.CharField(max_length=200)




class strategy(models.Model):
    url = models.SlugField(max_length=100, null=True, blank=True)

    level = models.CharField(max_length=100, null=True, blank=True)
    updatetime = models.CharField(max_length=100, null=True, blank=True)

    # method = models.CharField(max_length=500, null=True, blank=True)
    #
    # type = models.CharField(max_length=500, null=True, blank=True)

    addr = models.CharField(max_length=100, null=True, blank=True)

    content = models.CharField(max_length=1000, null=True, blank=True)

    province = models.CharField(max_length=50, null=True, blank=True)


    title = models.CharField(max_length=100, null=True, blank=True)

    intent = models.CharField(max_length=100, null=True, blank=True)

    talent = models.ManyToManyField(talentType)



class MethodAndType(models.Model):
    method = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    #通过MethodAndTyp查找政策的是用sta。如果不设置的话，是用默认的methodandtype_set(类名的小写+_set)
    stag = models.ForeignKey(strategy, on_delete=models.CASCADE, default='')




