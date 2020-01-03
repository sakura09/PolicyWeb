import json
import sqlite3
from django.db import models
import sys
import os

#from django.core.exceptions import ValidationError

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
# 找到根目录（与工程名一样的文件夹）下的settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

#没有处理脏读
import django

django.setup()

from policy.models import strategy,MethodAndType
from policy.models import talentType

#修改浙江省添加method的方法

with open('/Users/a123/Desktop/政策数据/浙江省数据(1).json', 'r', encoding='utf-8') as load_f:
    data = json.load(load_f)
    print("policy")

    count = 1
    #print(len(data['人才政策']))
    for line in data['人才政策']:
       # print(count)
        #print(type(line))
        #print(len(line))

        num = len(line)

        s = strategy()
        # print("2")
        # print(line)

        # s.method = line[1]['人才待遇']
        # s.type = line[2]['待遇类型']

        #浙江数据没有title，置空
        s.intent = line['待遇类型']
        s.level = '省级'
        s.addr = line['适用区域']
        s.content = line['政策条款及服务内容']
        s.url = line['政策原文链接']
        s.province = '浙江省'
        s.title = line['政策标题']
        #print(line['政策标题'])
        s.save()

        m = MethodAndType()
        # print(line[1]['人才待遇'])
        # print(line[2]['待遇类型'])
        m.method = line['人才待遇']
        m.type = line['待遇类型']
        m.province = '浙江省'
        m.stag = s
        m.save()
        # print("S")
        # print(m.method)
        # print(m.method)
        count = count + 1


        length = len(line['人才类别'])


with open('/Users/a123/Desktop/政策数据/t.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(len(data['省级政策']['广东省']))
    count = 1
    for line in data['国家级政策']:
        #print("H")
        #print(line)
        s = strategy()
        s.province = '国家级'
        s.level = '国家级'
        #print(line['url'])
        s.url = line['url']
        s.addr = '全国'
        s.updatetime = line['updatetime']
        s.title = line['info']['title']
        str = ''
        for i in line['info']['key_sentences']:
            str = str + i['text']
        s.content = str
        #s.intent = line['info']['key_sentences']['intent']
        print(str)
        s.save()
        #s.addr = line
        #外键数据项：先获取要插入的外键，然后和普通想一起插入


        for i in line['info']['key_sentences']:
            #是key_sentences的text还是slots的text
            for ob in i['slots']:
                print(ob)
                m = MethodAndType()
                m.method = ob['text']
                m.type = ob['type']
                m.province = '国家级'
                m.stag = s
           # m= MethodAndType(method=i['text'], type=i['intent'], stag=s)
                m.save()


        count  = count + 1
        # s.save()



    count = 0
    for line in data['省级政策']['广东省']:
        count = count+1
        #print("count")
        #print(count)
        #print("line")
        #print(line)
        s = strategy()
        s.addr = '广东省'
        s.level = '省级'
        s.province = '广东省'
        #print(line['url'])
        s.url = line['url']
        s.updatetime = line['updatetime']
        s.title = line['info']['title']
        str = ''
        for i in line['info']['key_sentences']:
            str = str + i['text']
        s.content = str
        print(str)
        # s.content = line['info']['key_sentences']['text']
        s.save()

        # s.addr = line
        for i in line['info']['key_sentences']:
            #是key_sentences的text还是slots的text
            for ob in i['slots']:
                print(ob)
                m = MethodAndType()
                m.method = ob['text']
                m.type = ob['type']
                m.province = '广东省'
                m.stag = s
           # m= MethodAndType(method=i['text'], type=i['intent'], stag=s)
                m.save()

    for line in data['省级政策']['江苏省']:
        #print('')
        count = count + 1
        s = strategy()
        s.level = '省级'
        s.addr = '江苏'
        s.province = '江苏省'
        # print(line['url'])
        s.url = line['url']
        s.updatetime = line['updatetime']
        s.title = line['info']['title']
        str = ''
        for i in line['info']['key_sentences']:
            str = str + i['text']
        s.content = str
        print(str)
        # s.content = line['info']['key_sentences']['text']
        s.save()

        # s.addr = line
        for i in line['info']['key_sentences']:
            # 是key_sentences的text还是slots的text
            for ob in i['slots']:
                print(ob)
                m = MethodAndType()
                m.method = ob['text']
                m.type = ob['type']
                m.province = '江苏省'
                m.stag = s
                # m= MethodAndType(method=i['text'], type=i['intent'], stag=s)
                m.save()

    for line in data['省级政策']['福建省']:
        #print('')
        count = count + 1
        s = strategy()
        s.addr = '福建省'
        s.level = '省级'
        s.province = '福建省'
        # print(line['url']s

        s.url = line['url']
        s.updatetime = line['updatetime']
        s.title = line['info']['title']
        str = ''
        for i in line['info']['key_sentences']:
            str = str + i['text']
        s.content = str
        print(str)
        # s.content = line['info']['key_sentences']['text']
        s.save()

        # s.addr = line
        for i in line['info']['key_sentences']:
            # 是key_sentences的text还是slots的text
            for ob in i['slots']:
                print(ob)
                m = MethodAndType()
                m.method = ob['text']
                m.type = ob['type']
                m.province = '福建省'
                m.stag = s
                # m= MethodAndType(method=i['text'], type=i['intent'], stag=s)
                m.save()


print("successful")






