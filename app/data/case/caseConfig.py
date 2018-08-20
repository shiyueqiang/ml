# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: caseConfig.py
@time: 2018/8/13 上午11:25
@desc:
"""
import json
class CaseConfig:

    @staticmethod
    def db_data():
        data= {
            'bc_module': '模块',
            'bc_version': '版本',
            'bc_prd': '需求名称',
            'bc_case_title': '用例标题',
            'bc_precondition': '前置条件',
            'bc_operate_steps': '操作步骤',
            'bc_expected_result': '预期结果',
            'bc_priority': '优先级',
            'bc_ispass': '执行结果',
            'bc_case_manager': '负责人',
            'bc_case_type': '业务测试用例'
        }
        return data

    @staticmethod
    def excel_data():
        data= {
            u'模块': 'bc_module',
            u'版本': 'bc_version',
            u'需求名称': 'bc_prd',
            u'用例标题': 'bc_case_title',
            u'前置条件': 'bc_precondition',
            u'操作步骤': 'bc_operate_steps',
            u'预期结果': 'bc_expected_result',
            u'优先级': 'bc_priority',
            u'执行结果': 'bc_ispass',
            u'负责人': 'bc_case_manager',
            u'用例类型': 'bc_case_type'
            }
        return data



case_config = CaseConfig

# print case_config.excel_data()['模块']

