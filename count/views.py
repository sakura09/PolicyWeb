from django.shortcuts import render

# Create your views here.
from django.core import paginator
from django.shortcuts import render

# Create your views here.
from django.db import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from policy.models import strategy
from django.http import HttpResponse, response
from django.http import JsonResponse
from django.core import serializers
import json

def getTalentNum(request):
    return JsonResponse

def getPolicyNum(request):
    return JsonResponse