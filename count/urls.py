from django.urls import path
from django.contrib import admin
from count.views import getTalentNum,getPolicyNum

#加方法
from policy.views import getAllPolicy

urlpatterns = [

    #新路由User
    path('getTalentNum/',  getTalentNum),

    path('getPolicyNum/',  getPolicyNum),

]
