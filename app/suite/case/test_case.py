# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: test_case.py
@time: 2018/8/14 上午10:15
@desc:
"""
from app.service.case.save import save
import os
from app.config.pathconfig import *
from app.utils.common import tools
from app import sqlPool, mydb

class TestCase:


    def __init__(self):
        self.sqlDatas = sqlPool['case']


    def save(self, files):
        """
        保存用例到数据库
        :return:
        """
        datas = tools.excel_to_db(tools.save_case_filepath(files))
        return save.save_db(datas)



    def query_all(self, arguments=None):
        """
        用例查询功能
        """
        sql = tools.get_sql(self.sqlDatas, 'select_all')
        try:
            if arguments['bc_module'] and arguments['bc_version']:
                newsql = sql + "where `bc_module` = '%s' and bc_version = '%s';" % (
                arguments['bc_module'], arguments['bc_version'])
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
        except Exception as e:
            tools.log().error(e)
            return '参数不全'


test_case = TestCase()