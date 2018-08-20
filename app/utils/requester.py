# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: requester.py
@time: 2018/7/31 上午11:17
@desc:
"""
import requests
from app.utils.common import tools
from app import config


class HttpRequester:

    def __init__(self):


        self.s = requests.Session()
        # 代理配置调试用
        if config['env']['model']:
            self.proxies = config['proxies']

        else:
            self.proxies = None

    def get_template(self, url, payload=None):
        """
        get请求模板
        """
        tools.log().info('接口请求get:  ' + str(url) + '  开始   ' + str(payload))
        try:
            try:
                res = self.s.get(url=url, params=payload, proxies=self.proxies)
                tools.log().info('接口返回: ' + res.json())
                return res.json()
            except Exception as e:
                tools.log().error(e)
                tools.log().info('接口返回: ')
                tools.log().info(res.text)
                return res.text
        except Exception as e:
            tools.log().error(e)

    def post_template(self, url, payload=None, filename=None):
        """
        post请求模板
        """
        tools.log().info('接口请求post:  ' + str(url) + '  开始   ' + str(payload))
        try:
            try:
                res = self.s.post(url=url, data=payload, files=filename, proxies=self.proxies)
                tools.log().info('接口返回: ' + res.json())
                return res.json()
            except Exception as e:
                tools.log().error(e)
                tools.log().info('接口返回: ')
                tools.log().info(res.text)
                return res.text
        except Exception as e:
            tools.log().error(e)



requester = HttpRequester()
