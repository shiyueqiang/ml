# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: query.py
@time: 2018/8/13 下午8:34
@desc:
"""
from app import mydb, sqlPool
from app.utils.common import tools
import json


class CaseQuery:

    def __init__(self):
        self.sqlDatas = sqlPool['case']

    def query_all(self, arguments=None):
        sql = tools.get_sql(self.sqlDatas, 'select_all')
        try:
            if arguments['bc_module'] and arguments['bc_version']:
                newsql = sql + "where `bc_module` = '%s' and bc_version = '%s' " % (
                    arguments['bc_module'], arguments['bc_version'])
                print newsql
                data = mydb.db_query(newsql)
            elif arguments['bc_module']:
                newsql = sql + "where `bc_module` = '%s';" % (arguments['bc_module'])
                data = mydb.db_query(newsql)
            elif arguments['bc_version']:
                newsql = sql + "where `bc_version` = '%s';" % (arguments['bc_version'])
                data = mydb.db_query(newsql)

            else:
                data = mydb.db_query(sql)
            return data
        except:
            return '参数不全'

case_query = CaseQuery()

if __name__ == '__main__':
    data = {'bc_module': '投资', 'bc_version': '1.0'}
    a = case_query.query_all(data)  # print json.dumps(a)
    print a