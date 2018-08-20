# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: commands.py
@time: 2018/8/2 下午4:07
@desc:
"""
import subprocess
import os
import time

class Command:

    @staticmethod
    def move(name):
        subprocess.Popen('mv ' + str(name) + ' /tmp', shell=True, cwd='/home/work')
        time.sleep(1)
        if os.path.exists('/tmp/' +str(name)):
            flag = '成功'
        else:
            flag = '失败'

        return flag