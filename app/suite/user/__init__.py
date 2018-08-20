# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: __init__.py.py
@time: 2018/8/2 下午3:33
@desc:
"""

from app import sqlYml
from app.utils.common import tools


# sql数据相关配置
sqlData = tools.get_yml(sqlYml)['sql']

