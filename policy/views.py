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

import json

#提前把数据加载到内存，提高查询效率
total_policy = strategy.objects.all()
total_method_policy = MethodAndType.objects.all()

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




#省份参数可以只有1个
def contrastPolicy(request):
    if request.method == 'GET':
        request.params = request.GET

    # 筛选条件, 传递普通数组
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
    print(index)



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
        l1 = l1.filter(q1)


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
            content = s.content
            url = s.url
            if url == 'null':
                url = ''
            method = line.method
            type = line.type
            data = {
                '政策标题': title,
                '适用区域': province,
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
            content = s.content
            url = s.url
            if url == 'null':
                url = ''
            method1 = line.method
            type1 = line.type
            data1 = {
                '政策标题': title,
                '适用区域': province,
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
            content = s.content
            url = s.url
            if url == 'null':
                url = ''
            method2 = line.method
            type2 = line.type
            data2 = {
                '政策标题': title,
                '适用区域': province,
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


#参数是选择的政策类别
def test2(method_type):
    print("test2")
    L = total_method_policy.filter(province='浙江省')
    print(L[0].stag_id)
    str = L[0].method
    print(str)


    #统计折线图的x, y轴数据
    pattern = re.compile(r'\d+万元')
    res = re.findall(pattern, str)
    p = re.compile(r'\d+')
    res2 = re.findall(p, res[0])
    res2 = int(res2[0])
    print(type(res2))
    print(res2)

    sum_p = [0 for _ in range(1000)]
    sum_p[2] = 3
    sum_p[999] = 999
    print(len(sum_p))
    print(sum_p[999])
    sum_p[2] = sum_p[2]+1
    print(sum_p[2])

    l1 = total_method_policy.filter(method = method_type)

    for line in l1:
        str = line.method
        pattern = re.compile(r'\d+万元')
        res = re.findall(pattern, str)
        pattern2 = re.compile(r'\d+亿元')
        res2 = re.findall((pattern2, str))
        # p2 = re.compile(r'\d+')
        # res2 = re.findall(p2, res[0])
        # res2 = int(res2[0])
        if len(res) > 0:
            for r in res:
                p2 = re.compile(r'\d+')
                r1 = re.findall(p2, r)
                r1= int(r1[0])
                sum_p[r1] = sum_p[r1]+1







