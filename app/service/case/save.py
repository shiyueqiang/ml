# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: test_case.py
@time: 2018/8/13 下午2:51
@desc:
"""
from app import mydb, sqlPool
from app.utils.common import tools
from app.config.pathconfig import tmpPath
import os
import json


class SaveCaseToDb:

    def __init__(self):

        self.sqlDatas = sqlPool['case']

    def get_version(self, bc_module):
        """
        根据模块获取版本号
        :param bc_module:
        :return:
        """
        data = mydb.db_query(tools.get_sql(self.sqlDatas, 'get_version', (bc_module,)), 1)
        return data

    def version_dict(self, datas):
        """
        获取每个模块最新版本号
        """

        module_list = []
        version_data = {}
        for module in datas:
            modules = datas[module]['bc_module']
            module_list.append(modules)
        module_list = list(set(module_list))
        for module in module_list:
            try:
                version_data[module] = float(str(self.get_version(module)['bc_version']))
            except:
                version_data[module] = 0.0
        for i in version_data:
            version_data[i] = round(version_data[i] + 0.1, 1)
        return version_data


    def save_db(self, datas):
        """
        读取excel文件保存到数据库
        版本根据module递增
        :param filename: excel文件地址
        :return:
        """
        flag = False
        version = self.version_dict(datas)
        for item in datas:
            bc_module = datas[item]['bc_module']
            bc_version = version[bc_module]
            bc_prd = datas[item]['bc_prd']
            bc_case_title = datas[item]['bc_case_title']
            bc_precondition = datas[item]['bc_precondition']
            bc_operate_steps = datas[item]['bc_operate_steps']
            bc_expected_result = datas[item]['bc_expected_result']
            bc_priority = datas[item]['bc_priority']
            bc_ispass = datas[item]['bc_ispass']
            bc_case_manager = datas[item]['bc_case_manager']
            bc_case_type = datas[item]['bc_case_type']
            mydb.db_insert(tools.get_sql(self.sqlDatas, 'save', (
            bc_module, bc_version, bc_prd, bc_case_title, bc_precondition, bc_operate_steps, bc_expected_result,
            bc_priority, bc_ispass, bc_case_manager, bc_case_type,)))
        for i in version:
            # 数字转化成同一类型进行比较
            if float(str(self.get_version(i)['bc_version'])) == version[i]:
                flag =True
                continue
            else:
                flag =False
                break
        if flag:
            return '保存成功'
        else:
            return '保存失败请看查看日志'


save = SaveCaseToDb()



if __name__ == '__main__':
    filename = os.path.join(tmpPath, 'test_case1.xlsx')
    datas = tools.excel_to_db(filename)
    a = save.save_db(datas)
    print a