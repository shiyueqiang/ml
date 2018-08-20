# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: __init__.py.py
@time: 2018/8/1 下午3:03
@desc:
"""
from app.utils.common import tools
from app.utils.db import DB
from app import sqlYml
from app.config.pathconfig import *


# 老用户相关初始化数据
ouserPath = os.path.join(dataPath, 'ouser')
ouser_sql = tools.get_yml(sqlYml)['ouser']

