"""
author:木木夕
date:2020-01-06 16:36
"""
from django.views import View
from django.http import HttpRequest,JsonResponse
from . import models
from utils import jsonify
import simplejson
import re
import logging
import math

FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

# 提取金额。 单位万元
def getIntmongey(strtemp:str,re_int):
    try:
        value = re_int.search(strtemp).groups()[0]
        value = value.strip(" ")
        if value[-1]=="万":
            return float(value[0:-1])
        elif value[-1]=="亿":
            return float(value[0:-1])*10000
        else:
            return float(value)/10000
    except Exception as e:
        print(e,re_int.match(strtemp))
        print(strtemp)
        return 0

# 政策对比
class PolicyAnalyze(View):

    # 获取折线图数据
    def getLinechart(self,tp,province):
        querylist = models.MethodAndType.objects.all()
        querylist = querylist.filter(province=province,type=tp).filter(method__contains="元")
        count = {"1000万以上":0,"100万~1000万":0,"50万~100万":0,"10万~50万":0,"1万~10万":0,"1万以下":0}
        re_int = re.compile(r"([0-9. ]*[万|亿]{0,1})元", re.X)
        for temp in querylist:
            value = getIntmongey(temp.method,re_int)
            if value>=1000:
                count["1000万以上"] += 1
            elif 1000 > value >= 100:
                count["100万~1000万"] += 1
            elif 100 > value >= 50:
                count["50万~100万"] += 1
            elif 50 >value >=10:
                count["10万~50万"] += 1
            elif 10 >value >=1:
                count["1万~10万"] += 1
            else:
                count["1万以下"] += 1
        return count

    # 获取雷达图数据
    def getRadarMap(self,province_list):
        data = {}
        querylist = models.MethodAndType.objects.all()
        max = querylist.count()
        data["max"] = max
        for i in province_list:
            value = querylist.filter(province=i).count()
            data[i] = {"value":value,"scale":math.ceil((value/max)*100)}
        return data

    def get(self,request:HttpRequest):
        payload = request.GET
        province_list = simplejson.loads(payload["province"]) # 政策区域
        # policyTypeList = simplejson.loads(payload["政策类型"]) # 政策类型
        serverTypeList = simplejson.loads(payload["服务类型"]) #服务类型

        if not province_list:
            return JsonResponse({"message":"type必选参数"})
        elif len(province_list)<=2:
            data_info = {}
            if serverTypeList[0]=="经费资助":
                data_info["ret"] = {i:self.getLinechart("经费资助",i) for i in province_list}
                data_info["data"] = self.getRadarMap(province_list)
            return JsonResponse(data_info)
        else:
            return JsonResponse({"message":"type最多只包含2个参数"})