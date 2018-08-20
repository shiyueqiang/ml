# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: common.py
@time: 2018/7/31 上午11:18
@desc:
"""
import csv
import logging
import logging.handlers
import random
import uuid
from decimal import Decimal
import json
import datetime
from dateutil.relativedelta import relativedelta
from flask import jsonify
from app.config.pathconfig import *
import os
import time
import yaml
from configparser import ConfigParser
import xlrd
from app.data.case.caseConfig import case_config


class CommonTools:

    @staticmethod
    def log():
        """
        日志输出到根目录下边的logs文件
        """
        logger = logging.getLogger()
        if not logger.handlers:
            LOG_FILE = os.path.join(logPath, time.strftime('%Y-%m-%d-%H', time.localtime(time.time())) + '.log')
            print LOG_FILE
            fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            formatter = logging.Formatter(fmt)
            handler = logging.handlers.RotatingFileHandler(LOG_FILE)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            return logger
        return logger

    @staticmethod
    def get_config(configPath):
        """
        获取配置.ini的配置文件
        """
        cfg = ConfigParser()
        cfg.read(configPath, encoding='utf-8')
        dictionary = {}
        for section in cfg.sections():
            dictionary[section] = {}
            for options in cfg.options(section):
                dictionary[section][options] = cfg.get(section, options)
        return dictionary

    @staticmethod
    def get_yml(ymlPath):
        """
        :param dataPath: 文件路径
        """
        return yaml.load(open(ymlPath, 'r'))

    @staticmethod
    def get_sql(datas, key, fills=None):
        """
        :param datas: sql语句池
        :param key: sql标签
        :param fills: 替换关键词
        :return: sql语句
        """
        if key in datas:
            sql = datas[key].replace('\n', '')
            return sql % fills if isinstance(fills, tuple) else sql

    @staticmethod
    def get_csv(filepath):
        """
        读取csv文件返回一个字典
        """
        with open(filepath, 'r') as f:
            read = csv.DictReader(f)
            data = []
            for rows in read:
                data.append(dict(rows))
            return data

    @staticmethod
    def get_json(filename):
        """
        读取config目录下的json文件
        """
        # file_name = json_name + ".json"
        # json_path = os.path.join(dataPath, file_name)
        data = json.loads(open(filename, 'r').read())
        return data

    @staticmethod
    def write_config(config_file, section, option, value):
        """
        写入ini配置文件
        """
        cfg = ConfigParser()
        cfg.read(config_file)
        cfg.set(section, option, value)
        cfg.write(open(config_file, 'w'))

    @staticmethod
    def write_csv(filename, headers, data):
        """
        以字典的格式多个写入文件
        """
        try:
            with open(filename, 'w') as f:
                writer = csv.DictWriter(f, headers)
                writer.writeheader()
                writer.writerows(data)  # 可以写多条
                print(str(file) + ' .csv文件  >>>>>>>>>>>>>>>>>>>>>  生成完毕')
        except Exception as e:
            print(e)
            print(str(file) + ' .csv文件  >>>>>>>>>>>>>>>>>>>>>  生成失败')

    @staticmethod
    def two_decimal(float_value):
        """
        保留两位小数点
        """
        return Decimal(float_value).quantize(Decimal("0.0"))

    @staticmethod
    def generate_sixcode():
        """
        获取6位验证数字
        """
        code_list = []
        for i in range(0, 9):
            code_list.append(str(i))
        mySlice = random.sample(code_list, 6)  # 生成6位随机数字
        verification_code = ''.join(mySlice)  # 转换成字符串的格式
        return verification_code

    @staticmethod
    def result(key, value):
        """
        对结果进行判断
        """
        if key == value:
            data = {'message': key, 'code': '200', 'status': 1, }
        else:
            data = {'message': key, 'code': '200', 'status': 0, }
        return jsonify(data)

    @staticmethod
    def timestamp():
        """
        获取当前时间戳如：20180801143901
        """
        t = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return int(t)

    @staticmethod
    def generate_uuid():
        """
        生成唯一流水号
        """
        return str(uuid.uuid1()).replace("-", "")

    @staticmethod
    def get_date_time(str_time, format="%Y-%m-%d"):
        """
        str(time) 转换datetime格式 年-月-日
        """
        return datetime.strptime(str_time, format)

    @staticmethod
    def get_str_time(date_time, format="%Y-%m-%d"):
        """
        datetime(time) 转换str格式 年-月-日
        """
        return datetime.strftime(date_time, format)

    @staticmethod
    def get_day_offset(start_date_time, end_date_time):
        """
        天数差值
        """
        return (end_date_time - start_date_time).days

    @staticmethod
    def get_month_offset(start_date_time, end_date_time):

        """
        月数差值
        时间格式都是datetime格式
        """
        year_offset = end_date_time.year - start_date_time.year
        month_offset = end_date_time.month - start_date_time.month
        return year_offset * 12 + month_offset

    @staticmethod
    def get_delta_date(base_date, year=0, month=0, day=0):
        """
        获取 添加指定年-月-日 后的时间
        输入:
            base_date: 基准日期

        方法自带逻辑：如该日期不存在，自动往前。比较2.29不存在，将
        返回2.28
        """
        return base_date + relativedelta(years=year, months=month, days=day)

    @staticmethod
    def analyze_time(year, month, day, hours, minute, seconds=None):
        """
        根据输入的年，月，日，时，分，秒.
        得到 2017-10-04 10:49:00 格式
        """
        return datetime(year, month, day, hours, minute, seconds)

    @staticmethod
    def get_time_offset(start_time, end_time):
        """
        获取时间差值包括天数时分秒
        """
        return end_time - start_time

    @staticmethod
    def duration2sec(string):
        """
        根据两个的日期差值，计算相差多少分钟
        利用split进行切片处理实现
        """
        if "days" in string:
            days = string.split()[0]
            hours = string.split()[2].split(':')
            return int(days) * 1440 + int(hours[0]) * 60 + int(hours[1]) + int(hours[2])
        else:
            hours = string.split(':')
            return int(hours[0]) * 60 + int(hours[1]) + int(hours[2])

    @staticmethod
    def get_data_minute(str_time, format='%Y-%m-%d %H:%M'):
        """
        获取datetime格式时间，格式年-月-日 时：分
        """

        return datetime.strptime(str_time, format)

    @staticmethod
    def get_path(path, name):
        """
        获取数据的路径
        :param path: 文件路径
        :param name: 文件名称
        :return: 绝对路径
        """
        return os.path.join(path, name)

    @staticmethod
    def check_params(arguements):
        """
        判断接口传过来的参数是否为空
        """
        return arguements if arguements else None

    @staticmethod
    def excel_to_db(filename):
        """
        将测试用例模板的数据解析成数据库对应的字段
        """
        wb = xlrd.open_workbook(filename)
        wt = wb.sheet_by_index(0)
        data = {}
        for i in range(1, wt.nrows):
            data['rows'+ str(i)] = {}
            for y in range(0, wt.ncols):
                data['rows'+ str(i)][case_config.excel_data()[wt.cell(0, y).value]] = wt.cell(i, y).value
        return data

    @staticmethod
    def save_case_filepath(files):
        """
        保存文件到服务器本地，返回文件地址
        :param files:
        :return:
        """
        # filename = files.filename + time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
        filename = files.filename
        fileinfo = os.path.splitext(filename)
        newfilenames = fileinfo[0]+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+fileinfo[-1]
        filepath = os.path.join(tmpPath, newfilenames)
        files.save(filepath)
        return filepath




tools = CommonTools()

#
# if __name__ == '__main__':
#     data = tools.get_config(envConfigPath)
#     print data
