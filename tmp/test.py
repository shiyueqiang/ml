# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: test.py
@time: 2018/7/31 下午4:58
@desc:
"""
from app.utils.common import tools
import os
from app.config.pathconfig import *
import json

filename = os.path.join(tmpPath, 'test_case1.xlsx')
a = tools.excel_to_db(filename)
print type(a)
for i in a:
    print a[i]
    b  = a[i]['bc_module']
    print b