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
    provinceList = request.GET.getlist('province', [])
    #provinceList = json.loads(provinceList)
    print(provinceList[0])
    #print(provinceList[1])

    policyTypeList = request.GET.getlist('政策类别', [])
    #policyTypeList = json.loads(policyTypeList[0])
    serverTypeList = request.GET.getlist('服务类型', [])
    print(serverTypeList[0])
    #serverTypeList = json.loads(serverTypeList[0])

    #页码不同
    #page_list = request.GET.get('pageNum1', [])
    num = request.GET.get('pageNum1', default='1')
    index = request.GET.get('pageNum2', default='1')
    #page_list = json.loads(page_list[0])
    print(num)
    try:
        index = (int(index) - 1) * 10
    except:
        index = (int(index) - 1) * 10
    index2 = index + 10
    num = (int(num) - 1) * 10
    print("页码2")

    # num1 = int(num)
    num2 = num+ 10
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
        l1 = l1.filter(q1)

        total_num = len([_ for _ in l1])
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
                '省份': province,
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
                '省份': province,
                '人才待遇': method1,
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
                '省份': province,
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
        result = JsonResponse({'total_num1': total_num1, 'total_num2': total_num2, 'treatList1': r1, 'treatList2': r2},
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

