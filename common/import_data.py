import sys
import os
#from common.models import Policy
import json
import sqlite3

conn = sqlite3.connect('db.sqlite3')
#c = conn.cursor()
print('Open database successfully')

#conn.execute()

with open('/Users/a123/Desktop/浙江.json', 'r', encoding='utf-8') as load_f:
    data = json.load(load_f)
    for line in data['浙江']:
        #print("H")
        #print(line['info']['categoryName'])
        #break

        sql = "insert into policy(updatetime, url , categoryName, method, type, addr, categoryContent) " \
              "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (line['updatetime'],  line['url'],line['info']['categoryName'],
                                                           line['info']['method'], line['info']['type'],line['info']['addr']
                                                           ,line['info']['categoryContent'])
        #c.execute(sql)
        conn.execute(sql)
        conn.commit()


#查询记录
#curosr = conn.execute('select url from zhejiang_policy')


print('Successful')
#conn.close()