"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.urls import include
#加方法
from policy.views import getAllPolicy,contrastPolicy,test,op,test2,zxt,area,radar1,radar2,\
    zxt_city,radar1_city,radar2_city,radar3_city

urlpatterns = [
    path('admin/', admin.site.urls),

    #新路由User
    path('api/policy/op', op),
    path('api/policy/getAllPolicy',  getAllPolicy),

    path('api/policy/contrastPolicy', contrastPolicy),
    path('api/policy/test', test),
    path('api/policy/test2', test2),

    path('api/policy/zxt', zxt),
    #path('api/policy/area', area),
    path('api/policy/radar1', radar1),
    path('api/policy/radar2', radar2),

    path('api/policy/zet_city',zxt_city),
    path('api/policy/radar1_city',radar1_city),
    path('api/policy/radar2_city',radar2_city),
    path('api/policy/radar3_city',radar3_city)


    #path('count/', inlcude('count.urls')),
    #路由manger
    #path('mgr/', include('mgr.urls')),

]
