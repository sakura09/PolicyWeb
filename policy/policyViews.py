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


# def test(request:HttpRequest):
#     t1 = {"经费资助", "生活补贴", "引才补助", "担保贷款"}  # 经济补贴
#     t2 = {"周转住房", "购房补贴", "租房补贴", "安家补贴", "人才公寓"}  # 住房保障
#     t3 = {"户籍保障", "家属就业", "医疗保健", "社会保险", "综合服务", "子女教育"}  # 服务保障
#     querylist = models.MethodAndType.objects.all()
#     from django.db.models import Count
#     # querylist = querylist.values("type","province").annotate(num=Count("id"))
#     # data_info = {}
#     # for i in querylist:
#     #     province = i["province"]
#     #     tp = i["type"]
#     #     num = i["num"]
#     #     if province not in data_info:
#     #         data_info[province] = {"经济补贴":0,"住房保障":0,"服务保障":0,"其他":0}
#     #     if tp in t1:
#     #         data_info[province]["经济补贴"] += num
#     #     elif tp in t2:
#     #         data_info[province]["住房保障"] += num
#     #     elif tp in t3:
#     #         data_info[province]["服务保障"] += num
#     #     else:
#     #         data_info[province]["其他"] += num
#     #     # data_info[province][i["type"]] = i["num"]
#     # print(data_info)
#
#     querylist = querylist.values("type").annotate(num=Count("id"))
#     data_info = {"经济补贴":0,"住房保障":0,"服务保障":0,"其他":0}
#     for i in querylist:
#         tp = i["type"]
#         num = i["num"]
#         if tp in t1:
#             data_info["经济补贴"] += num
#         elif tp in t2:
#             data_info["住房保障"] += num
#         elif tp in t3:
#             data_info["服务保障"] += num
#         else:
#             data_info["其他"] += num
#     print(data_info)
#     return JsonResponse(data_info)