from django.urls import path
#加方法
from policy.views import getAllPolicy,op,contrastPolicy,test

urlpatterns = [
    path('getAllPolicy/', getAllPolicy),
    path('contrastPolicy', contrastPolicy),
    path('test', test),
    path('op/', op),
]