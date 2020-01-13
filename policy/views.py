from django.core import paginator
from django.db.models import F
from django.shortcuts import render

# Create your views here.
from django.db import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from policy.models import strategy,talentType,MethodAndType
from django.http import HttpResponse, response
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
import re
from itertools import chain

import json

#提前把数据加载到内存，提高查询效率
total_policy = strategy.objects.all()
total_method_policy = MethodAndType.objects.all()
L_zj = total_policy.filter(province="浙江省")
L_zj2 = total_method_policy.filter(province="浙江省")

import datetime
from collections import OrderedDict

class LruCatch():
    lru_cache = {}
    __sef__ = None

    def __new__(cls, *args,**kwargs):
        if not cls.__sef__:
            self = super().__new__(cls, *args, **kwargs)
            cls.__sef__ = self
        return cls.__sef__

    # 设置缓存
    def catch_set(self,fnname:str,stt:str,rest):
        if not self.lru_cache.get(fnname, None):
            self.lru_cache[fnname] = OrderedDict()
        length = len(self.lru_cache[fnname].keys())
        if length >= 100:
            key = None
            for i in self.lru_cache[fnname]:
                key = i
                break
            self.lru_cache[fnname].pop(key)
        self.lru_cache[fnname][stt] = (datetime.datetime.now(), rest)

    # 获取缓存
    def catch_get(self,fnname:str,stt:str):
        if not self.lru_cache.get(fnname,None):
            self.lru_cache[fnname] = OrderedDict()
        return self.lru_cache[fnname].get(stt,None)

def op(request):
    data = 'hello world'
    return JsonResponse({'data': data})

#分页输出
def getAllPolicy(request):
    #request.params = json.loads(request.body)

    # 获取去全部政策数据家, all()返回的是QuerySet对象
    print("start")
    page_num = request.GET.get('pageNum', default='1')
    print("页码")
    print(page_num)

    page_num1 = (int(page_num) - 1) * 10
    page_num2 = page_num1 + 10
    print(page_num1)
    print(page_num2)
    #
    page_list = total_policy[page_num1: page_num2]

    method_list = []
    type_list = []
    ret = []
    print("page_len")
    print(len(page_list))
    for line in page_list:
        mlist = MethodAndType.objects.filter(stag_id=line.id)
        for m in mlist:
            method_list.append(m.method)
            type_list.append(m.type)
        #type_list = m.type
        #print(line.url)
        addr = line.addr
        title = line.title
        url = line.url
        content = line.content
        data = {
            '政策标题':title,
            '人才待遇':method_list,
            '待遇类型':type_list,
            '适用区域':addr,
            '政策条款及服务内容':content,
            'url':url
        }

        ret.append(data)

    ret = JsonResponse({'retList': ret}, json_dumps_params={'ensure_ascii': False})
    ret["Access-Control-Allow-Origin"] = "http://192.168.1.12:8080"
    ret["Access-Control-Allow-Credentials"] = "true"
    ret["Access-Control-Allow-Methods"] = "GET,POST"
    ret["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
    return ret



def zxt(t, provinceList):
    print(t)
    print(provinceList)
    dataList = []

    if len(provinceList) == 1:
        L = total_method_policy.filter(province=provinceList[0])
        l1 = L.filter(type=t)
        l2 = []
    elif len(provinceList) == 2:
        L = total_method_policy.filter(province=provinceList[0])
        L2 = total_method_policy.filter(province=provinceList[1])
        l1 = L.filter(type=t)
        l2 = L2.filter(type=t)



    p1 = re.compile(r'\d+元')
    p2 = re.compile(r'\d+\.?\d万元')
    p3 = re.compile(r'\d+\.?\d万')
    p4 = re.compile(r'\d+亿元')

    result1 = [0 for _ in range(6)]
    result2 = [0 for _ in range(6)]

    print(len(l1))
    print(len(l2))
    if len(l1)>0 and len(l2)==0:
        print("1")
        for line in l1:
            temp1 = re.findall(p1, line.method)
            len1 = len(temp1)
            if len1 > 0:
                result1[0] = result1[0]+1

            temp2 = re.findall(p2, line.method)
            len2 = len(temp2)
            temp3 = re.findall(p3, line.method)
            len3 = len(temp3)
            if len2 > 0 or len3 > 0:
                for i in temp2:
                    p = re.compile(r'\d+\.?\d')
                    res2 = re.findall(p, i)
                    res2 = float(res2[0])
                    if res2>=1 and res2<10:
                        result1[1] = result1[1]+1
                    elif res2>=10 and res2<50:
                        result1[2] = result1[2]+1
                    elif res2>=50 and res2<100:
                        result1[3] = result1[3]+1
                    elif res2>=100 and res2<1000:
                        result1[4] = result1[4]+1

            temp4 = re.findall(p4, line.method)
            len4 = len(temp4)
            if len4 > 0:
                result1[5] = result1[5]+1
                # for i in temp4:
                #     p = re.compile(r'\d+')
                #     res2 = re.findall(p, i)
                #     res2 = int(res2[0]) * 10000
        #计算面积
        area1 = (result1[0]+result1[1])*10/2
        area2 = (result1[1]+result1[2])*10/2
        area3 = (result1[2]+result1[3])*20/2
        area4 = (result1[3]+result1[4])*30/2
        area5 = (result1[4]+result1[5])*40/2
        Area1 = area1+area2+area3+area4+area5

        data1 = {
            "1万以下": result1[0],
            "1-10": result1[1],
            "10-50": result1[2],
            "50-100": result1[3],
            "100-1000": result1[4],
            "1000-1亿": result1[5]
        }
        dataList.append(data1)
        print(data1)
        #ret = JsonResponse({"data1":data1})
        return dataList



    if len(l2) > 0:
        print("2")
        print(len(l1))
        print(len(l2))

        for line in l1:
            temp1 = re.findall(p1, line.method)
            len1 = len(temp1)
            if len1 > 0:
                result1[0] = result1[0] + 1

            temp2 = re.findall(p2, line.method)
            len2 = len(temp2)
            temp3 = re.findall(p3, line.method)
            len3 = len(temp3)
            if len2 > 0 or len3 > 0:
                for i in temp2:
                    p = re.compile(r'\d+\.?\d')
                    res2 = re.findall(p, i)
                    res2 = float(res2[0])
                    if res2 >= 1 and res2 < 10:
                        result1[1] = result1[1] + 1
                    elif res2 >= 10 and res2 < 50:
                        result1[2] = result1[2] + 1
                    elif res2 >= 50 and res2 < 100:
                        result1[3] = result1[3] + 1
                    elif res2 >= 100 and res2 < 1000:
                        result1[4] = result1[4] + 1

            temp4 = re.findall(p4, line.method)
            len4 = len(temp4)
            if len4 > 0:
                result1[5] = result1[5] + 1

        for line in l2:
            temp1 = re.findall(p1, line.method)
            len1 = len(temp1)
            if len1 > 0:
                result2[0] = result2[0] + 1

            temp2 = re.findall(p2, line.method)
            len2 = len(temp2)
            temp3 = re.findall(p3, line.method)
            len3 = len(temp3)
            if len2 > 0 or len3 > 0:
                for i in temp2:
                    p = re.compile(r'\d+\.?\d')
                    res2 = re.findall(p, i)
                    res2 = float(res2[0])
                    if res2 >= 1 and res2 < 10:
                        result2[1] = result2[1] + 1
                    elif res2 >= 10 and res2 < 50:
                        result2[2] = result2[2] + 1
                    elif res2 >= 50 and res2 < 100:
                        result2[3] = result2[3] + 1
                    elif res2 >= 100 and res2 < 1000:
                        result2[4] = result2[4] + 1

            temp4 = re.findall(p4, line.method)
            len4 = len(temp4)
            if len4 > 0:
                result2[5] = result2[5] + 1

        # 计算面积
        area1 = (result2[0] + result2[1]) * 10 / 2
        area2 = (result2[1] + result2[2]) * 10 / 2
        area3 = (result2[2] + result2[3]) * 20 / 2
        area4 = (result2[3] + result2[4]) * 30 / 2
        area5 = (result2[4] + result2[5]) * 40 / 2
        Area2 = area1 + area2 + area3 + area4 + area5

        data1 = {
            "1万以下":result1[0],
            "1-10":result1[1],
            "10-50":result1[2],
            "50-100":result1[3],
            "100-1000":result1[4],
            "1000-1亿":result1[5]
        }
        data2 = {
            "1万以下": result2[0],
            "1-10": result2[1],
            "10-50": result2[2],
            "50-100": result2[3],
            "100-1000": result2[4],
            "1000-1亿": result2[5]
        }

        print(data1)
        print(data2)
        dataList.append(data1)
        dataList.append(data2)
        #ret = JsonResponse({"data1":data1,"data2":data2})
        return dataList

#数量指标
def radar1(typeList, provinceList):
    print(typeList)
    print(provinceList)
    if len(provinceList) == 1:
        print("1")
        dataList = []
        print(provinceList[0])
        l1 = total_method_policy.filter(province=provinceList[0])
        #valueList = [0 for _ in range(len(typeList))]
        i = 0
        for t in typeList:
            L = total_method_policy.filter(type=t)
            max = len(L)
            temp1 = l1.filter(type=t)
            value1 = len(temp1)
            scale1 = (value1/max) * 100
            #valueList[i] = value1

            data = {
                "max":max,
                "value1":value1,
                "scale1":scale1,
            }
            dataList.append(data)
            i = i+1

        #ret = JsonResponse({"dataList":dataList})
        return dataList

    if len(provinceList) == 2:
        print("2")
        dataList = []
        #dataList2 = []
        l1 = total_method_policy.filter(province=provinceList[0])
        l2 = total_method_policy.filter(province=provinceList[1])
        print(len(l1))
        print(len(l2))
        #valueList = []
        #i = 0
        for t in typeList:
            L = total_method_policy.filter(type=t)
            print(t)
            max = len(L)
            temp1 = l1.filter(type=t)
            temp2 = l2.filter(type=t)
            value1 = len(temp1)
            scale1 = (value1/max)* 100
            value2 = len(temp2)
            scale2 = (value2/max)*100
            print(value1)
            print(value2)
            #valueList[i] = value1

            data = {
                "max":max,
                "value1":value1,
                "scale1":scale1,
                "value2":value2,
                "scale2":scale2
            }
            dataList.append(data)
            #i = i+1
        print(dataList[0])
        print(dataList[1])
        #ret = JsonResponse({"dataList": dataList})
        return dataList



def area(t, List):

    # l1 = total_method_policy.filter(province=p)
    #print(len(List))
    l1 = []
    for line in List:
        if t == line.type:
            l1.append(line)
    #l1 = List.filter(type=t)
    #print(len(l1))
    p1 = re.compile(r'\d+元')
    p2 = re.compile(r'\d+\.?\d*万元')
    p3 = re.compile(r'\d+\.?\d*万')
    p4 = re.compile(r'\d+亿元')

    result1 = [0 for _ in range(6)]
    result2 = [0 for _ in range(6)]
    if len(l1) > 0:

        for line in l1:
            #print(line.method)
            temp1 = re.findall(p1, line.method)
            len1 = len(temp1)
            #print(len1)
            if len1 > 0:
                #print("in1")
                result1[0] = result1[0] + 1

            temp2 = re.findall(p2, line.method)
            len2 = len(temp2)
            #print("len2")
            #print(len2)
            temp3 = re.findall(p3, line.method)
            len3 = len(temp3)
            #print("len3")
            #print(len3)
            if len2 > 0 or len3 > 0:
                #print("in")
                for i in temp2:
                    p = re.compile(r'\d+\.?\d*')
                    res2 = re.findall(p, i)
                    res2 = float(res2[0])
                    if res2 >= 1 and res2 < 10:
                        result1[1] = result1[1] + 1
                    elif res2 >= 10 and res2 < 50:
                        result1[2] = result1[2] + 1
                    elif res2 >= 50 and res2 < 100:
                        result1[3] = result1[3] + 1
                    elif res2 >= 100 and res2 < 1000:
                        result1[4] = result1[4] + 1

            temp4 = re.findall(p4, line.method)
            len4 = len(temp4)
            if len4 > 0:
                result1[5] = result1[5] + 1

        #print("result1")
        #print(result1)
        # 计算面积
        area1 = (result1[0] + result1[1]) * 10 / 2
        area2 = (result1[1] + result1[2]) * 10 / 2
        area3 = (result1[2] + result1[3]) * 20 / 2
        area4 = (result1[3] + result1[4]) * 30 / 2
        area5 = (result1[4] + result1[5]) * 40 / 2
        Area = area1 + area2 + area3 + area4 + area5

        return Area


#力度雷达图
def radar2(typeList, provinceList):
    print(typeList)
    print(provinceList)
    if len(provinceList)==1:
        print("1")
        dataList=[]
        l1 = total_method_policy.filter(province=provinceList[0])
        for t in typeList:
            L = total_method_policy.filter(type=t)
            max_area = area(t, L)
            temp1 = l1.filter(type=t)
            value1 = area(t, temp1)
            scale1 = (value1/max_area) * 100

            data = {
                "max":max_area,
                "value1":value1,
                "scale1":scale1
            }
            dataList.append(data)

        ret = JsonResponse({"dataList":dataList})
        return ret


    if len(provinceList)==2:
        print("2")
        dataList = []
        l1 = total_method_policy.filter(province=provinceList[0])
        l2 = total_method_policy.filter(province=provinceList[1])
        print(len(l1))
        print(len(l2))
        dataList=[]
        for t in typeList:
            L = total_method_policy.filter(type=t)
            print(t)
            max_area = area(t, L)
            print("max")
            print(max_area)

            temp1 = l1.filter(type=t)
            print("temp1")
            print(len(temp1))
            temp2 = l2.filter(type=t)
            print("temp2")
            print(len(temp2))
            value1 = area(t, temp1)
            print("value1")
            print(value1)
            scale1 = (value1/max_area) * 100
            value2 = area(t, temp2)
            print("value2")
            print(value2)
            scale2 = (value2/max_area) * 100


            data = {
                "max":max_area,
                "value1":value1,
                "scale1":scale1,
                "value2":value2,
                "scale2":scale2
            }

            dataList.append(data)

        print(dataList[0])
        print(dataList[1])
        ret = JsonResponse({"dataList":dataList})
        return ret

#市级折线图
#t, cityList, p
def zxt_city(request):
    t = request.GET.get('type', '')
    p = request.GET.get('province', '')
    cityList = request.GET.get('cityList', [])
    cityList = json.loads(cityList)

    catch = LruCatch()
    stt = "".join(cityList) + t + p
    fnname = "zxt_city"
    value = catch.catch_get(fnname,stt)
    if value:
        return  value[1]

    a = [0, 0.5, 1, 5, 10, 15, 20, 25, 30, 40, 50, 60, 90, 95, 100, 300, 500, 1000, 10000]
    A = ['0-0.5','0.5-1','1-5','5-10','10-15','15-20','20-25','25-30','30-40','40-50','50-60','60-90','90-95','95-100'
         , '100-300','300-500','500-1000','1000-一亿']
    b1 = [0 for _ in range(18)]
    b2 = [0 for _ in range(18)]

    L = total_policy.filter(province=p)
    print(p)
    print("L.len")
    print(len(L))
    dataList = []
    List1=[]
    List2=[]
    if len(cityList) == 1:
        print("city1")
        city1 = cityList[0]

        i = 0
        for line in L:
            str1 = line.addr
            str = str1.encode()
            temp = str.decode('utf-8')
            pattern = "[\u4e00-\u9fa5]+市"  # 中文正则表达式
            p = re.compile(pattern)  # 生成正则对象
            results = p.findall(temp)
            if len(results) == 0:
                continue
            if city1 == results[0]:
                stagId = line.id
                L1 = total_method_policy.filter(stag_id=stagId)
                L1 = L1.filter(type=t)
                for l in L1:
                    List1.append(l)

                i = i + 1


    elif len(cityList) == 2:

        print(cityList)
        city1 = cityList[0]
        city2 = cityList[1]

        i = 0
        j = 0
        for line in L:
            str1 = line.addr
            str = str1.encode()
            temp = str.decode('utf-8')
            # print("temp")
            # print(temp)
            pattern = "[\u4e00-\u9fa5]+市"  # 中文正则表达式
            p = re.compile(pattern)  # 生成正则对象
            results = p.findall(temp)
            #print(results)
            if len(results) == 0:
                continue
            if city1 == results[0]:
                stagId = line.id
                L1 = total_method_policy.filter(stag_id=stagId)
                L1 = L1.filter(type=t)
                for l in L1:
                    List1.append(l)

                i = i+1

            elif city2 == results[0]:
                stagId = line.id
                L2 = total_method_policy.filter(stag_id=stagId)
                L2 = L2.filter(type = t)
                for l in L2:
                    List2.append(l)

                j = j+1
        print("i,j")
        print(i)
        print(j)
        print(type(List1))
        print(len(List1))
        print(List2[0].method)
        print(len(List2))
        print(List2[0].method)



        print("list1.len")
        print(len(List1))
        print("list2.len")
        print(len(List2))

    #全选
    else:
        l1 = total_method_policy.filter(province=p)
        List1 = l1.filter(type=t)
        List2 = []



    p1 = re.compile(r'\d+元')
    p2 = re.compile(r'\d+\.?\d万元')
    p3 = re.compile(r'\d+\.?\d万')
    p4 = re.compile(r'\d+亿元')

    result1 = [0 for _ in range(6)]
    result2 = [0 for _ in range(6)]
    for line in List1:
        #print("list1")
        temp1 = re.findall(p1, line.method)
        # p = re.compile(r'\d+')
        # res2 = re.findall(p, temp1)
        # res2 = int(res2[0])

        if len(temp1) > 0:
            for i in temp1:
                p = re.compile(r'\d+\.?\d')
                res2 = re.findall(p, i)
                if len(res2) == 0:
                    continue
                res2 = float(res2[0])
                res2 = res2/10000
                if res2>a[0] and res2<a[1]:
                    b1[0] = b1[0]+1
                elif res2>a[1] and res2<a[2]:
                    b1[1] = b1[1]+1

        temp2 = re.findall(p2, line.method)
        len2 = len(temp2)
        temp3 = re.findall(p3, line.method)
        len3 = len(temp3)
        if len2 > 0 or len3 > 0:
            #?
            temp2 = temp2+temp3
            for i in temp2:
                p = re.compile(r'\d+\.?\d')
                res2 = re.findall(p, i)
                if len(res2) == 0:
                    continue
                res2 = float(res2[0])
                for j in range(len(a)):
                    # print("i")
                    # print(i)
                    if res2 > a[j] and res2<=a[j+1]:
                        b1[j] =b1[j]+1

        temp4 = re.findall(p4, line.method)
        len4 = len(temp4)
        if len4 > 0:
            for i in temp4:
                p = re.compile(r'\d+\.?\d')
                res2 = re.findall(p, i)
                if len(res2) == 0:
                    continue
                # print(type(res2))
                # print(res2)
                res2 = float(res2[0])
                res2 = res2 * 10000
                if res2>=a[18]:
                    b1[17] = b1[17]+1


    if len(List2) > 0:
        print("list2.len > 0")
        for line in List2:
            # print("list1")
            temp1 = re.findall(p1, line.method)
            # p = re.compile(r'\d+')
            # res2 = re.findall(p, temp1)
            # res2 = int(res2[0])

            if len(temp1) > 0:
                for i in temp1:
                    p = re.compile(r'\d+\.?\d')
                    res2 = re.findall(p, i)
                    if len(res2) == 0:
                        continue

                    res2 = float(res2[0])
                    res2 = res2 / 10000
                    if res2 > a[0] and res2 < a[1]:
                        b2[0] = b2[0] + 1
                    elif res2 > a[1] and res2 < a[2]:
                        b2[1] = b2[1] + 1

            temp2 = re.findall(p2, line.method)
            len2 = len(temp2)
            temp3 = re.findall(p3, line.method)
            len3 = len(temp3)
            if len2 > 0 or len3 > 0:
                # ?
                temp2 = temp2 + temp3
                for i in temp2:
                    p = re.compile(r'\d+\.?\d')
                    res2 = re.findall(p, i)
                    if len(res2) == 0:
                        continue
                    res2 = float(res2[0])
                    for j in range(len(a)):
                        # print("i")
                        # print(i)
                        if res2 > a[j] and res2 <= a[j + 1]:
                            b2[j] = b2[j] + 1

            temp4 = re.findall(p4, line.method)
            len4 = len(temp4)
            if len4 > 0:
                for i in temp4:
                    p = re.compile(r'\d+\.?\d')
                    res2 = re.findall(p, i)
                    if len(res2) == 0:
                        continue
                    res2 = float(res2[0])
                    res2 = res2 * 10000
                    if res2 >= a[18]:
                        b2[17] = b2[17] + 1




        ret = JsonResponse({"a":A, "b1":b1, "b2":b2},json_dumps_params={'ensure_ascii': False})

    else :
        # data1 = {
        #     "1万以下": result1[0],
        #     "1-10": result1[1],
        #     "10-50": result1[2],
        #     "50-100": result1[3],
        #     "100-1000": result1[4],
        #     "1000-1亿": result1[5]
        # }
        # dataList.append(data1)
        ret = JsonResponse({"a":A, "b1":b1},json_dumps_params={'ensure_ascii': False})

    print("a")
    print(A)
    print("b1")
    print(b1)
    print("b2")
    print(b2)

    catch.catch_set(fnname,stt,ret)

    return  ret

#市级数量雷达图
#typeList, cityList, p
def radar1_city(request):
    typeList = request.GET.get('typeList')
    print(len(typeList))
    print(typeList)
    #print(typeList[0])
    typeList = json.loads(typeList)
    print(len(typeList))
    print(typeList[0])
    print("p1")
    p = request.GET.get('province')
    print(p)
    cityList = request.GET.get('cityList')
    #print(cityList)
    cityList = json.loads(cityList)

    print(len(cityList))
    print(cityList)
    catch = LruCatch()
    fnname = "radar1_city"
    stt = "{}-{}-{}".format(typeList,p,cityList)
    value = catch.catch_get(fnname,stt)
    if value:
        return value[1]
    L = total_policy.filter(province=p)
    dataList=[]
    List = []
    List1 = []
    List2=[]
    newL1 = []
    newL2 = []
    newL = []
    if len(cityList)==1:
        a1 = ['max', 'value1', 'scale1']
        print("city1")
        city1 = cityList[0]

        i = 0
        x = 0
        for line in L:
            str1 = line.addr
            str = str1.encode()
            temp = str.decode('utf-8')
            pattern = "[\u4e00-\u9fa5]+市"  # 中文正则表达式
            p = re.compile(pattern)  # 生成正则对象
            results = p.findall(temp)
            if len(results) == 0:
                continue
            if city1 == results[0]:
                stagId = line.id
                l1 = total_method_policy.filter(stag_id = stagId)
                for l in l1:
                    List1.append(l)
                i = i + 1

            sId = line.id
            l = total_method_policy.filter(stag_id=sId)
            for m in l:
                List.append(m)

            x = x+1

        for t in typeList:

            for line in List:
                if t == line.type:
                    newL.append(line)
            max = len(newL)
            for line in List1:
                if t == line.type:
                    newL1.append(line)
            value1 = len(newL1)
            scale1 = (value1/max)*100


            max1 = 100
            # data = [0 for _ in range(3)]
            # data[0] = max
            # data[1] = value1
            # data[2] = scale1
            data = {
                "max":max1,
                "value1":value1,
                "scale1":scale1,
                "name":t
            }
            dataList.append(data)

        print(len(dataList))
        print(dataList[0])
        ret = JsonResponse({"a1":a1, "dataList":dataList}, json_dumps_params={'ensure_ascii': False})
        catch.catch_set(fnname, stt, ret)
        return ret

    elif len(cityList) == 2:
        a2 = ['max', 'value1', 'scale1', 'value2', 'scale2']
        print("city2")
        city1 = cityList[0]
        city2 = cityList[1]

        i = 0
        j = 0
        x = 0
        for line in L:
            str1 = line.addr
            str = str1.encode()
            temp = str.decode('utf-8')
            pattern = "[\u4e00-\u9fa5]+市"  # 中文正则表达式
            p = re.compile(pattern)  # 生成正则对象
            results = p.findall(temp)
            if len(results) == 0:
                continue
            if city1 == results[0]:
                stagId = line.id
                l1 = total_method_policy.filter(stag_id=stagId)
                for l in l1:
                    List1.append(l)

                i = i + 1

            elif city2 == results[0]:
                stagId = line.id
                l2 = total_method_policy.filter(stag_id=stagId)
                for l in l2:
                    List2.append(l)

                j = j + 1

            # sId = line.id
            # l = total_method_policy.filter(stag_id=sId)
            # for m in l:
            #     List.append(m)

            x = x + 1

        for t in typeList:

            # for line in List:
            #     if t == line.type:
            #         newL.append(line)
            # print(len(List1))
            # print(len(List2))
            # max = len(List1)+len(List2)
            # print("max")
            # print(max)
            max = len(List1)+len(List2)
            print(max)
            print(len(List1))
            print(len(List2))
            for line in List1:
                if t == line.type:
                    newL1.append(line)
            value1 = len(newL1)
            scale1 = (value1/max) * 100

            for line in List2:
                if t == line.type:
                    newL2.append(line)
            value2 = len(newL2)
            scale2 = (value2/max) * 100



            max1 = 100
            # data = [0 for _ in range(5)]
            # data[0] = max
            # data[1] = value1
            # data[2] = scale1
            # data[3] = value2
            # data[4] = scale2
            data = {
                "max":max1,
                # "value1":scale1,
                "value1":value1,
                "scale1":scale1,
                # "value2":scale2,
                "value2": value2,
                # "scale2":value2,
                "scale2":scale2,
                "name":t
            }
            dataList.append(data)

        print(len(dataList))
        print(dataList[0])
        ret = JsonResponse({"a2":a2, "dataList":dataList}, json_dumps_params={'ensure_ascii': False})
        catch.catch_set(fnname, stt, ret)
        return ret

    else :
        a1 = ['max', 'name']
        L = total_method_policy.filter(province = p)
        for t in typeList:
            for line in L:
                if t == line.type:
                    newL.append(line)
            max = len(newL)
            max1 = 100
            data = {
                "max": max1,
                "value":max,
                "scale":100,
                "name": t
            }
            dataList.append(data)

        print(len(dataList))
        print(dataList[0])
        ret = JsonResponse({"a1": a1, "dataList": dataList}, json_dumps_params={'ensure_ascii': False})
        catch.catch_set(fnname, stt, ret)
        return ret




#市级力度雷达图
#typeList, cityList, p
def radar2_city(request):
    typeList = request.GET.get('typeList', [])
    typeList = json.loads(typeList)
    p = request.GET.get('province', '')
    cityList = request.GET.get('cityList', [])
    cityList = json.loads(cityList)

    catch = LruCatch()
    fnname = "radar2_city"
    stt = "{}-{}-{}".format(typeList,p,cityList)
    value = catch.catch_get(fnname,stt)
    if value:
        return value[1]

    L = total_policy.filter(province=p)
    print(len(L))
    dataList = []
    List = []
    List1 = []
    List2 = []
    if len(cityList) == 1:
        a1 = ['max', 'value1', 'scale1']
        print("city1")
        city1 = cityList[0]

        i = 0
        x = 0
        for line in L:
            str1 = line.addr
            str = str1.encode()
            temp = str.decode('utf-8')
            pattern = "[\u4e00-\u9fa5]+市"  # 中文正则表达式
            p = re.compile(pattern)  # 生成正则对象
            results = p.findall(temp)
            if len(results) == 0:
                continue
            if city1 == results[0]:
                stagId = line.id
                l1 = total_method_policy.filter(stag_id=stagId)
                for l in l1:
                    List1.append(l)

                i = i + 1

            sId = line.id
            l = total_method_policy.filter(stag_id=sId)
            for m in l:
                List.append(m)

            x = x + 1

        for t in typeList:

            max_area = area(t, List)
            value1 = area(t, List1)
            scale1 = (value1/max_area) * 100
            # data = [0 for _ in range(3)]
            # data[0] = max_area
            # data[1] = value1
            # data[2] = scale1
            max1 = 100
            data = {
                "max":max1,
                "value1":value1,
                "scale1":scale1,
                "name":t
            }
            dataList.append(data)

        print("1city")
        print(len(dataList))
        print(dataList[0])
        ret = JsonResponse({"a1":a1, "dataList":dataList}, json_dumps_params={'ensure_ascii': False})
        catch.catch_set(fnname,stt,ret)
        return ret


    elif len(cityList) == 2:
        a2 = ['max', 'value1', 'scale1', 'value2', 'scale2']
        print("city2")
        city1 = cityList[0]
        city2 = cityList[1]

        i=0
        j=0
        x=0
        for line in L:
            str1 = line.addr
            str = str1.encode()
            temp = str.decode('utf-8')
            pattern = "[\u4e00-\u9fa5]+市"  # 中文正则表达式
            p = re.compile(pattern)  # 生成正则对象
            results = p.findall(temp)
            if len(results) == 0:
                continue
            if city1 == results[0]:
                stagId = line.id
                l1 = total_method_policy.filter(stag_id=stagId)
                for l in l1:
                    List1.append(l)
                i = i + 1
            elif city2 == results[0]:
                stagId = line.id
                l2 = total_method_policy.filter(stag_id=stagId)
                for l in l2:
                    List2.append(l)
                j = j + 1

            # sId = line.id
            # l = total_method_policy.filter(stag_id=sId)
            # for m in l:
            #     List.append(m)
            x = x + 1

        for t in typeList:
            #print("in")
            max_area1 = area(t, List1)
            max_area2 = area(t, List2)
            max_area = max_area1+max_area2
            #print("max")
            #print(max_area)
            value1 = area(t, List1)
            #print("v1")
            #print(value1)
            scale1 = (value1/max_area) * 100
            value2 = area(t, List2)
            #print("v2")
            #print(value2)
            scale2 = (value2/max_area) * 100

            max1 = 100
            # data = [0 for _ in range(5)]
            # data[0] = max_area
            # data[1] = value1
            # data[2] = scale1
            # data[3] = value2
            # data[4] = scale2
            data = {
                "max":100,
                "value1":value1,
                "scale1":scale1,
                "value2":value2,
                "scale2":scale2,
                "name":t
            }
            dataList.append(data)
        print("2city")
        print(len(dataList))
        #print(dataList[0])
        ret = JsonResponse({"a2":a2, "dataList":dataList}, json_dumps_params={'ensure_ascii': False})
        catch.catch_set(fnname, stt, ret)
        return ret

    else:
        a1 = ['max', 'name']
        L = total_method_policy.filter(province=p)
        for t in typeList:
            max_area = area(t, L)
            max1 = 100
            data = {
                "max": max1,
                "value":max_area,
                "scale":100,
                "name": t
            }
            dataList.append(data)

        print(len(dataList))
        #print(dataList[0])
        ret = JsonResponse({"a1": a1, "dataList": dataList}, json_dumps_params={'ensure_ascii': False})
        catch.catch_set(fnname, stt, ret)
        return ret


#市级得分雷达图图
#typeList, cityList, p
def radar3_city(request):
    typeList = request.GET.get('typeList', [])
    typeList = json.loads(typeList)
    p = request.GET.get('province', '')
    cityList = request.GET.get('cityList', [])
    cityList = json.loads(cityList)
    catch = LruCatch()
    stt = "{}-{}".format(typeList,cityList)
    fnname = "radar3_city"
    value = catch.catch_get(fnname,stt)
    if value:
        return value[1]

    #L = total_policy.filter(province=p)
    L = L_zj
    print(len(L))
    dataList = []
    indicator = []
    #value1 = [0 for _ in range(typeList)]
    #value2 = [0 for _ in range(typeList)]

    List = []
    List1 = []
    List2 = []
    newL = []
    newL1 = []
    newL2 = []

    if len(cityList) == 1:
        a1 = ['max', 'value1', 'scale1']
        print("city1")
        city1 = cityList[0]
        for line in L:
            str1 = line.addr
            str = str1.encode()
            temp = str.decode('utf-8')
            pattern = "[\u4e00-\u9fa5]+市"  # 中文正则表达式
            p = re.compile(pattern)  # 生成正则对象
            results = p.findall(temp)
            if len(results) == 0:
                continue
            if city1 == results[0]:
                stagId = line.id
                l1 = total_method_policy.filter(stag_id=stagId)
                for l in l1:
                    List1.append(l)

            sId = line.id
            l = total_method_policy.filter(stag_id=sId)
            for m in l:
                List.append(m)

        for t in typeList:
            for line in List:
                if t == line.type:
                    newL.append(line)
            for line in List1:
                if t == line.type:
                    newL1.append(line)
            m1 = len(newL)
            m2 = area(t, List)
            max = m1*m2
            v1 = len(newL1)
            v2 = area(t, List1)
            value1 = v1*v2
            scale1 = (value1/max) * 100

            max1 = 100
            # data = [0 for _ in range(3)]
            # data[0]
            # data[0] = max
            # data[1] = value1
            # data[2] = scale1
            data = {
                "max":max1,
                "value1":value1,
                "scale1":scale1,
                "name":t
            }
            dataList.append(data)

        print('1个City')
        print(len(dataList))
        #print(dataList[0])
        ret = JsonResponse({"a1":a1, "dataList":dataList}, json_dumps_params={'ensure_ascii': False})
        catch.catch_set(fnname,stt,ret)
        return ret



    elif len(cityList) == 2:
        a2 = ['max', 'value1', 'scale1', 'value2', 'scale2']
        print(cityList)
        city1 = cityList[0]
        city2 = cityList[1]


        for line in L:
            str1 = line.addr
            str = str1.encode()
            temp = str.decode('utf-8')
            pattern = "[\u4e00-\u9fa5]+市"  # 中文正则表达式
            p = re.compile(pattern)  # 生成正则对象
            results = p.findall(temp)
            if len(results) == 0:
                continue
            if city1 == results[0]:
                stagId = line.id
                l1 = total_method_policy.filter(stag_id=stagId)
                #List1 = list(l1)
                for l in l1:
                    List1.append(l)

            elif city2 == results[0]:
                stagId = line.id
                l2 = total_method_policy.filter(stag_id=stagId)
                #List2 = list(l2)
                for l in l2:
                    List2.append(l)

            ##
            # sId = line.id
            # #L = MethodAndType.objects.raw('selec')
            # l = L_zj2.filter(stag_id=sId)
            # for m in l:
            #     List.append(m)


        i=0
        for t in typeList:
            # for line in List:
            #     if t == line.type:
            #         newL.append(line)
            for line in List1:
                if t == line.type:
                    newL1.append(line)
            for line in List2:
                if t == line.type:
                    newL2.append(line)
            m1 = len(List1)+len(List2)
            List = List1+List2
            m2 = area(t, List)
            max = m1*m2
            v1 = len(newL1)
            v2 = area(t, List1)
            value1 = v1*v2
            scale1 = (value1/max) * 100
            x1 = len(newL2)
            x2 = area(t, List2)
            value2 = x1 * x2
            scale2 = (value2/max) * 100

            max1 = 100
            data = {
                "max": max1,
                "value1": value1,
                "scale1": scale1,
                "value2": value2,
                "scale2": scale2,
                "name": t
            }
            dataList.append(data)
        ret = JsonResponse({"a2":a2, "dataList":dataList}, json_dumps_params={'ensure_ascii': False})
        print('两个City')
        print(len(dataList))
        #print(dataList[0])
        catch.catch_set(fnname, stt, ret)
        return ret

    else:
        print("全省")
        a1 = ['max', 'name']
        L = total_method_policy.filter(province = p)
        for t in typeList:
            for line in L:
                if t == line.type:
                    newL.append(line)
            m1 = len(newL)
            m2 = area(t, L)
            max = m1 * m2
            max1 = 100
            data = {
                "max":max1,
                "value":max,
                "sacle":100,
                "name":t
            }
            dataList.append(data)
        ret = JsonResponse({"a1": a1, "dataList": dataList}, json_dumps_params={'ensure_ascii': False})
        catch.catch_set(fnname, stt, ret)
        return ret






#省份参数可以只有1个
def contrastPolicy(request):
    if request.method == 'GET':
        request.params = request.GET

    # 筛选条件, 传递普通数组
    #新增城市数组 new
    cityList = request.GET.getlist('cityList',[])
    cityList = json.loads(cityList[0])
    # print(cityList)


    #省份数组
    provinceList = request.GET.getlist('province', [])
    #provinceList = request.GET.get('province', '')
    provinceList = json.loads(provinceList[0])
    print(provinceList[0])
    #print(provinceList[1])

    #政策类型数组
    policyTypeList = request.GET.getlist('政策类型', [])
    policyTypeList = json.loads(policyTypeList[0])
    #服务类型数组
    serverTypeList = request.GET.getlist('服务类型', [])
    print(serverTypeList[0])
    serverTypeList = json.loads(serverTypeList[0])

    #页码不同
    pageList = request.GET.getlist('pageNum', [])
    pageList = json.loads(pageList[0])
    if len(pageList) == 1:
        num = pageList[0]
        num = (int(num) - 1) * 10
        num2 = num + 10
        print("只有一个页码")
    elif len(pageList) == 2:
        num = pageList[0]
        index =pageList[1]
        print(num)
        try:
            index = (int(index) - 1) * 10
        except:
            index = (int(index) - 1) * 10
        index2 = index + 10
        num = (int(num) - 1) * 10
        num2 = num + 10
        print("页码2")

    # num1 = int(num)
    print("num_2")
    print(num2)


    print(provinceList)
    print(policyTypeList)
    print(serverTypeList)
    print(num)
    # print(index)
    stt = "{}-{}-{}-{}".format(provinceList,policyTypeList,serverTypeList,num)
    catch = LruCatch()
    fnname = "contrastPolicy"
    value = catch.catch_get(fnname,stt)
    if value:
        return value[1]



    #只有一个省份
    if len(provinceList) == 1:
        print("H")
        print("prov")
        print(provinceList)
        print(len(provinceList))
        print("type")
        print(policyTypeList)
        print(len(policyTypeList))
        print("serv")
        print(serverTypeList)
        print(len(serverTypeList))

        l1 = total_method_policy.filter(province=provinceList[0])
        print('l1.len')
        print(len([_ for _ in l1]))
        q1 = Q()
        q1.connector = 'OR'
        if policyTypeList:
            for i in policyTypeList:
                #    l1 = l1.filter(intent=i)
                q1.children.append(('type', i))


        if serverTypeList:
            for i in serverTypeList:
                #    l1 = l1.filter(intent=i)
                q1.children.append(('type', i))



        print('q1.len')
        print(len(q1))
        print(q1)
        l1 = l1.filter(q1)

        # new
        List=[]
        List1=[]
        List2=[]

        if len(cityList)>0 and len(cityList)<=2:
            print("in1")
            city1 = cityList[0]
            print("city1")
            print(city1)
            for line in L_zj:
                str1 = line.addr
                str = str1.encode()
                temp = str.decode('utf-8')
                pattern = "[\u4e00-\u9fa5]+市"  # 中文正则表达式
                p = re.compile(pattern)  # 生成正则对象
                results = p.findall(temp)
                if len(results) == 0:
                    continue
                if city1 == results[0]:
                    stagId = line.id
                    print(stagId)
                    l1 = total_method_policy.filter(stag_id=stagId)
                    #l1 = l1.distance()
                    for l in l1:
                        List1.append(l)

                elif len(cityList) == 2:
                    city2 = cityList[1]
                    # print("city2")
                    # print(city2)
                    if city2 == results[0]:
                        stagId = line.id
                        l2 = total_method_policy.filter(stag_id=stagId)
                        # l1 = l1.distance()
                        for l in l2:
                            List2.append(l)
            List = List1+List2
            print(len(List1))
            print(len(List2))
            print(len(List))


            newL = []
            dataList = []
            for t in serverTypeList:
                for line in List:
                    if line.type == t:
                        newL.append(line)

            total_num = len([_ for _ in newL])
            for line in newL[num:num2]:
                s = strategy.objects.get(id=line.stag_id)
                title = s.title
                province = s.province
                addr = s.addr
                content = s.content
                url = s.url
                if url == 'null':
                    url = ''
                method = line.method
                type = line.type
                data = {
                    '政策标题': title,
                    '适用区域': addr,
                    '人才待遇': method,
                    'url': url,
                    '政策条款及服务内容': content,
                    '待遇类型': type
                }
                dataList.append(data)
            print(len(dataList))
            ret = JsonResponse({'total_num': total_num, 'retList': dataList}, json_dumps_params={'ensure_ascii': False})

            catch.catch_set(fnname,stt,ret)
            return ret
        # elif len(cityList)>2:
        #     print("in3")
        #     for line in L_zj:
        #         str1 = line.addr
        #         str = str1.encode()
        #         temp = str.decode('utf-8')
        #         pattern = "[\u4e00-\u9fa5]+市"  # 中文正则表达式
        #         p = re.compile(pattern)  # 生成正则对象
        #         results = p.findall(temp)
        #         if len(results) == 0:
        #             continue
        #         List.append(line)
        #
        #     newL = []
        #     dataList = []
        #     for t in serverTypeList:
        #         for line in List:
        #             if line.type == t:
        #                 newL.append(line)
        #     total_num = len([_ for _ in newL])
        #     for line in newL[num:num2]:
        #         s = strategy.objects.get(id=line.stag_id)
        #         title = s.title
        #         province = s.province
        #         addr = s.addr
        #         content = s.content
        #         url = s.url
        #         if url == 'null':
        #             url = ''
        #         method = line.method
        #         type = line.type
        #         data = {
        #             '政策标题': title,
        #             '适用区域': addr,
        #             '人才待遇': method,
        #             'url': url,
        #             '政策条款及服务内容': content,
        #             '待遇类型': type
        #         }
        #         dataList.append(data)
        #     print(len(dataList))
        #     ret = JsonResponse({'total_num': total_num, 'retList': dataList}, json_dumps_params={'ensure_ascii': False})
        #     return ret

        total_num = len([_ for _ in l1])
        print('total_num')
        print(total_num)
        method_list = []
        type_list = []

        data_list = []
        for line in l1[num:num2]:
            s = strategy.objects.get(id = line.stag_id)
            title = s.title
            province = s.province
            addr = s.addr
            content = s.content
            url = s.url
            if url == 'null':
                url = ''
            method = line.method
            type = line.type
            data = {
                '政策标题': title,
                '适用区域': addr,
                '人才待遇': method,
                'url': url,
                '政策条款及服务内容': content,
                '待遇类型': type
            }
            data_list.append(data)
        r1 = data_list

        print("r1")
        print(len(r1))
        ret = JsonResponse({'total_num': total_num, 'retList': r1}, json_dumps_params={'ensure_ascii': False})
        ret["Access-Control-Allow-Origin"] = "http://192.168.1.12:8080"
        ret["Access-Control-Allow-Credentials"] = "true"
        ret["Access-Control-Allow-Methods"] = "GET,POST"
        ret["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
        catch.catch_set(fnname,stt,ret)
        return ret

    #两个省份
    if len(provinceList) == 2:
        print("F")
        l1 = total_method_policy.filter(province=provinceList[0])
        l2 = total_method_policy.filter(province=provinceList[1])
        print(len([_ for _ in l1]))
        print(len([_ for _ in l2]))
        #print(type(l1))



        q1 = Q()
        q1.connector = 'OR'
        if policyTypeList:
            for i in policyTypeList:
                #    l1 = l1.filter(intent=i)
                #q1.children.append(('intent', i))
                #根据方法表的类型搜索
                q1.children.append(('type', i))

        if serverTypeList:
            for i in serverTypeList:
                #    l1 = l1.filter(intent=i)
                #q1.children.append(('intent', i))
                q1.children.append(('type', i))

        print('类型')
        print(q1)
        l1 = l1.filter(q1)
        l2 = l2.filter(q1)


        print(len([_ for _ in l1]))
        print(len([_ for _ in l2]))
        total_num1 = len([_ for _ in l1])
        total_num2 = len([_ for _ in l2])

        data1_list = []
        data2_list = []

        for line in l1[num:num2]:
            s = strategy.objects.get(id = line.stag_id)
            title = s.title
            province = s.province
            addr = s.addr
            content = s.content
            url = s.url
            if url == 'null':
                url = ''
            method1 = line.method
            type1 = line.type
            data1 = {
                '政策标题': title,
                '适用区域': addr,
                '人才待遇1': method1,
                'url': url,
                '政策条款及服务内容': content,
                '待遇类型': type1
            }
            data1_list.append(data1)
        r1 = data1_list

        for line in l2[index:index2]:
            s = strategy.objects.get(id = line.stag_id)
            title = s.title
            province = s.province
            addr = s.addr
            content = s.content
            url = s.url
            if url == 'null':
                url = ''
            method2 = line.method
            type2 = line.type
            data2 = {
                '政策标题': title,
                '适用区域': addr,
                '人才待遇': method2,
                'url': url,
                '政策条款及服务内容': content,
                '待遇类型': type2
            }
            data2_list.append(data2)
        r2 = data2_list

        print("r1")
        print(len(r1))
        print("r2")
        print(len(r2))
        result = JsonResponse({'total_num1': total_num1, 'total_num2': total_num2, 'treat1': r1, 'treatList2': r2},
                              json_dumps_params={'ensure_ascii': False})
        #
        result["Access-Control-Allow-Origin"] = "http://192.168.1.12:8080"
        result["Access-Control-Allow-Credentials"] = "true"
        result["Access-Control-Allow-Methods"] = "GET,POST"
        result["Access-Control-Allow-Headers"] = "Origin,Content-Type,Cookie,Accept,Token"
        # ret = 0 对比成功
        catch.catch_set(fnname,stt,result)
        return result



def test(request):
    L = total_method_policy.filter(province='福建省')
    print(L[0].stag_id)
    x = L[0].stag_id
    # x = int(x)
    # print(type(x))
    m = strategy.objects.get(id=L[0].stag_id)
    list1=[]
    list2=[]
    # for ob in m:
    #     list1.append(ob.method)
    #     list2.append(ob.type)
    print(type(m))
    title = m.title
    print(m.id)
    print(L[0].method)
    print(L[1].method)
    # print(m[0].method)
    # print(m[1].method)

    #ret = JsonResponse({'method_list':list1, 'type_list':list2}, json_dumps_params={'ensure_ascii': False})
    ret = JsonResponse({'title':title},json_dumps_params={'ensure_ascii': False})
    return ret
    #m.stag
    # m.type
    # m.method
    # print(m.type)
    # print(m.method)



#
def test2(request):
    # print("test2")
    # L = total_method_policy.filter(province='浙江省')
    # print(type(L))
    # print(L[0].stag_id)
    # str = L[0].method
    # print(str)
    #
    #
    # #统计折线图的x, y轴数据
    # pattern = re.compile(r'\d+万元')
    # res = re.findall(pattern, str)
    # p = re.compile(r'\d+')
    # res2 = re.findall(p, res[0])
    # res2 = int(res2[0])
    # print(type(res2))
    # print(res2)
    #
    # sum_p = [0 for _ in range(1000)]
    # sum_p[2] = 3
    # sum_p[999] = 999
    # print(len(sum_p))
    # print(sum_p[999])
    # sum_p[2] = sum_p[2]+1
    # print(sum_p[2])
    #
    # l1 = total_method_policy.filter(method = method_type)
    #
    # for line in l1:
    #     str = line.method
    #     pattern = re.compile(r'\d+万元')
    #     res = re.findall(pattern, str)
    #     pattern2 = re.compile(r'\d+亿元')
    #     res2 = re.findall((pattern2, str))
    #     # p2 = re.compile(r'\d+')
    #     # res2 = re.findall(p2, res[0])
    #     # res2 = int(res2[0])
    #     if len(res) > 0:
    #         for r in res:
    #             p2 = re.compile(r'\d+')
    #             r1 = re.findall(p2, r)
    #             r1= int(r1[0])
    #             sum_p[r1] = sum_p[r1]+1
    #     t = '经费资助'
    #     p = ['浙江省', '广东省']
    #     zxt(t, p)

    # str = "每人每年4万元"
    # p2 = re.compile(r'\d+\.?\d*万元')
    # #p2 = re.compile(r'\d+万元')
    # p = re.findall(p2, str)
    # print(p)
    # print("--")
    # typeList = ['生活补贴']
    # provinceList = ['浙江省', '福建省']
    # radar2(typeList, provinceList)
    # List = total_method_policy.filter(province = "福建省")
    # area("生活补贴", List)
    # print("---")
    # str = "台州市天台县".encode()
    #
    # temp = str.decode('utf-8')
    # print(type(temp))
    # pattern="[\u4e00-\u9fa5]+市"#中文正则表达式
    # p = re.compile(pattern) #生成正则对象
    # results = p.findall(temp)
    # print(results)
    # print("----")
    # typeList=["经费资助", "生活补贴"]
    # p = "浙江省"
    # cityList=["台州市","杭州市"]
    # #zxt_city("经费资助", cityList, p)
    # radar1_city(typeList,cityList,p)

    print("---------")
    a = [0,1,10,20,30,40,50,60,70,80,90,100,500,1000,10000]
    b = [0 for _ in range(14)]
    temp = 0
    pro = "浙江省"
    L = total_method_policy.filter(province=pro)
    p1 = re.compile(r'\d+元')
    p2 = re.compile(r'\d+\.?\d万元')
    p3 = re.compile(r'\d+\.?\d万')
    p4 = re.compile(r'\d+亿元')

    print(len(a))
    l1 = L.filter(type="经费资助")
    print(len(l1))
    print("L.len")
    print(len(L))
    for line in L:
        temp1 = re.findall(p1, line.method)
        # p = re.compile(r'\d+')
        # res2 = re.findall(p, temp1)
        # res2 = int(res2[0])

        if len(temp1) > 0:
            for i in range(len(temp1)):
                temp = temp + 1

        temp2 = re.findall(p2, line.method)
        len2 = len(temp2)
        temp3 = re.findall(p3, line.method)
        len3 = len(temp3)
        if len2 > 0 or len3 > 0:
            temp2 = temp2 + temp3
            #print(temp2)
            for i in temp2:
                p = re.compile(r'\d+\.?\d')
                res2 = re.findall(p, i)
                res2 = float(res2[0])
                for j in range(len(a)):
                    # print("i")
                    # print(i)
                    if res2 > a[j] and res2<=a[j+1]:
                        b[j] =b[j]+1

        temp4 = re.findall(p4, line.method)
        len4 = len(temp4)
        if len4>0:
            for i in range(len(temp4)):
                b[13] = b[13]+1

    print(temp)
    print(b)

    # print("test sql")
    # #L = MethodAndType.objects.raw('select id')
    # idList = []
    # for line in strategy.objects.raw('select * form strategy where province = '浙江省''):
    #     stagId = line.id
    #     idList.append(stagId)
    # print("idList.len")
    # print(len(idList))
    #
    # List = []
    # for sid in idList:
    #     L = MethodAndType.objects.raw('SELECT * FROM MethodAndType where id = sID')
    #     List.append(L)
    # print("List.len")
    # print(len(List))


#扩展性接口
#def extendInterface():

