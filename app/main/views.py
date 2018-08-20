# coding:utf-8
"""
@version:
@author: shiyueqiang
@file: views.py
@time: 2018/8/2 下午3:49
@desc:
"""
from . import *
from app.suite.command.commands import Command
from app.suite.case.test_case import test_case
from app.utils.common import tools
from flask import jsonify, request
import os





@service.route('/move', methods=['GET', 'POST'])
def move():
    """
    linux移动文件
    """
    if tools.check_params(request.args):
        fromData = request.args.get('name')
        return result(Command.move(fromData), '成功')
    else:
        return jsonify({'msg': '参数不能为空'})


@service.route('/caseList', methods=['GET', 'POST'])
def case_list():
    """
    linux移动文件
    """
    if tools.check_params(request.args):
        fromData = request.args
        data = fromData.to_dict()
        return jsonify(test_case.query_all(data))
    else:
        return jsonify({'msg': '参数不能为空'})


@service.route('/caseUpload', methods=['GET', 'POST'])
def upload_case():
    """
    文件上传保存到数据库
    :return:
    """
    if tools.check_params(request.files):
        files = request.files.get('file')
        return tools.result(test_case.save(files), '保存成功')
    else:
        return jsonify({'msg': '参数不能为空'})


@main.route('/', methods=['GET', 'POST'])
def test():
    """
    测试用
    """
    data = {'message': 'SUCCESS', 'code': '200', 'status': 1, }
    return jsonify(data)
