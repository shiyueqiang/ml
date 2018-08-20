# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: __init__.py.py
@time: 2018/7/30 上午10:41
@desc:
"""
from flask import Blueprint

main = Blueprint('main', __name__)
user = Blueprint('user', __name__)
service = Blueprint('service', __name__)
test = Blueprint('test', __name__)

from . import views


