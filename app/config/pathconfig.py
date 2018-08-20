# coding:utf-8
"""
@version:
@author: shiyueqiang
@file: pathconfig.py
@time: 2018/7/31 下午1:34
@desc: 路径相关配置
"""
import os

# 基础目录
BasePath = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

# 当前目录
configPath = os.path.split(__file__)[0]

# 根目录
RootPath = os.path.split(BasePath)[0]

# 日志目录
logPath = os.path.join(RootPath, 'logs')

# 环境配置文件
envConfigPath = os.path.join(configPath, 'config.ini',)

# 依赖数据基础目录
dataPath = os.path.join(BasePath, 'data')

# sql数据
sqlPath = os.path.join(dataPath,'sql')

# 临时目录
tmpPath = os.path.join(RootPath, 'tmp')

# print tmpPath, dataPath
