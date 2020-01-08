from django.urls import path,re_path
#加方法
from policy.views import getAllPolicy,op,contrastPolicy,test
from .policyViews import PolicyAnalyze

# 路由：url = api/policy/ + 下面路由
urlpatterns = [
    re_path('^getAllPolicy$', getAllPolicy),
    re_path('^contrastPolicy$', contrastPolicy),
    re_path('^test$', test),
    re_path('^op$', op),
    re_path("^policyanalyze$",PolicyAnalyze.as_view())
]