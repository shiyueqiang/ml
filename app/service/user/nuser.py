# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: nuser.py
@time: 2018/8/1 下午4:55
@desc:
"""
import yaml
import json
import os
import requests
import datetime
import uuid
import logging
import random
import time
from bs4 import BeautifulSoup
from app.utils.common import tools

# 脚本执行目录
BASE_DIR = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

# 发送注册验证短信数据
SEND_CODE_FILE = os.path.join(os.path.split(BASE_DIR)[0], 'data/nuser/sendCode.json')


# 用户注册数据
REGISTER_FILE = os.path.join(os.path.split(BASE_DIR)[0], 'data/nuser/register.json')

# 用户开户请求数据
OPEN_BANK_ACCOUNT_FILE = os.path.join(os.path.split(BASE_DIR)[0], 'data/nuser/open_bank_account.json')

# 用户设置登录密码数据
SET_PASSWD_FILE = os.path.join(os.path.split(BASE_DIR)[0], 'data/nuser/set_passwd.json')

# 配置文件
CONFIG_FILE = os.path.join(os.path.split(BASE_DIR)[0], 'data/nuser/config.yml')





class XWCreate:

    def __init__(self, mobile, money, platform):
        """
        初始化数据
        """
        self.sendCode_data = json.loads(open(SEND_CODE_FILE).read())
        self.u_id = None
        self.user_key = None
        self.token = None
        self.bank_card = None
        self.mobile = mobile
        self.money = money
        self.platform = platform
        self.update_platform()
        self.register_data = json.loads(open(REGISTER_FILE).read())
        self.set_passwd_data = json.loads(open(SET_PASSWD_FILE).read())
        self.open_bank_account_data = json.loads(open(OPEN_BANK_ACCOUNT_FILE).read())
        self.config = yaml.load(open(CONFIG_FILE, 'r'))

    def update_platform(self):
        """
        更新测试商编
        """
        config = yaml.load(open(CONFIG_FILE, 'r'))
        config['dlan_payload']['platformNo'] = self.platform
        return yaml.dump(config, open(CONFIG_FILE, 'w'))


    def timestamp(self):
        """
        获取当前时间戳
        """
        t = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return int(t)

    def unix_timestamp(self):
        """
        获取当前时间戳unix 10位
        """
        return int(time.time())

    def failtime(self):
        """
        授权时间
        """
        t = datetime.datetime.now().strftime('%Y%m%d')
        return int(t)

    def mobile_hide(self):
        """
        手机号隐藏中间4位
        """
        str_mobile = str(self.mobile)
        remove_data = str_mobile[3:-4]
        return str_mobile.replace(remove_data, '****')

    def bank_card_tail(self):
        """
        银行卡后四位
        """
        return self.bank_card[-4:]

    def generate_uuid(self):
        """
        生成唯一流水号
        """
        return str(uuid.uuid1()).replace("-", "")

    def requests_template(self, url, data):
        """
        请求模板
        """
        r = requests.post(url=url, data=data, verify=False)
        try:
            if r.status_code == 200:
                return r.json()
            else:
                tools.log().debug('request' + r.url + 'post' + r.text)
        except:
            # tools.log().debug(r.text)
            return r.text

    def generate_sign(self, data):
        """
            生成签名
            """
        url = 'http://127.0.0.1:8090/xw-sdk-web/api/getSign.do'
        payload = {'debug': 1, 'respData': str(data)}
        res = requests.get(url=url, params=payload)
        try:
            tools.log().debug(res.json())
            return res.json()['sign']
        except:
            pass

    def send_code(self):
        """
        发送注册验证码
        """
        # print self.mobile
        payload = self.sendCode_data
        payload['fun']['sendVerifyCode']['mobile'] = self.mobile
        payload['statics']['timestamp'] = self.unix_timestamp()
        res = self.requests_template(url=self.config['config']['url'], data=json.dumps(payload))
        if res['sendVerifyCode']['error_code'] == 0:
            # print res
            return True
        else:
            # print res
            return False

    def user_register(self):
        """
        金蛋平台注册
        """
        payload = self.register_data
        payload['fun']['register']['mobile'] = self.mobile
        payload['statics']['timestamp'] = self.unix_timestamp()
        res = self.requests_template(url=self.config['config']['url'], data=json.dumps(payload))
        if res['register']['error_code'] == 0:
            self.u_id = res['register']['data']['user_id']
            self.token = res['register']['data']['token']
            self.user_key = res['register']['data']['userKey']
        else:
            print '注册失败:' + str(res)

    def set_passwd(self):
        """
        设置登录密码
        """
        payload = self.set_passwd_data
        payload['statics']['user_id'] = self.user_key
        payload['statics']['token'] = self.token
        payload['statics']['timestamp'] = self.unix_timestamp()
        res = self.requests_template(url=self.config['config']['url'], data=json.dumps(payload))
        if res['set_password']['error_code'] == 0:
            print '设置密码成功'
        else:
            print '设置密码失败'

    def get_request_key(self):
        """
        获得新网requestKey
        """
        self.send_code()
        self.user_register()
        self.set_passwd()
        url = 'https://xwbk.lanmaoly.com/bha-neo-app/lanmaotech/gateway'
        payload = self.config['INVEST_PERSONAL_REGISTER_EXPAND']['req_data']
        payload['timestamp'] = str(self.timestamp())
        payload['platformUserNo'] = str(self.u_id)
        payload['requestNo'] = str(self.generate_uuid())
        payload['failTime'] = str(self.failtime())
        payload['amount'] = '1000000'
        sign = self.generate_sign(str(payload))
        register_data = self.config['dlan_payload']
        register_data['serviceName'] = 'PERSONAL_REGISTER_EXPAND'
        register_data['reqData'] = str(payload)
        register_data['sign'] = str(sign)
        res = self.requests_template(url=url, data=register_data)
        soup = BeautifulSoup(res, "html.parser")
        a = soup.find_all('input')
        for link in a:
            b = link.get('value')
            if b:
                c = b.encode('unicode-escape').decode('string_escape')
                if c:
                    if '-' in c and '/' not in c:
                        tools.log().info(c)
                        self.key = c
                        return c

    def send_sms(self):
        """
        注册发送验证码
        """
        self.get_request_key()
        print self.key
        url = 'https://xwbk.lanmaoly.com/bha-neo-app/gateway/sms/smsForEnterprise'
        payload = {'requestKey': self.key, 'bizType:': 'REGISTER', 'mobile': self.mobile

                   }
        print payload
        res = self.requests_template(url=url, data=payload)
        print res
        try:
            if res.json()['status'] == 'SUCCESS':
                return True
        except:
            return False

    def register(self):
        """
        新网开户
        """
        self.send_sms()
        self.bank_card = str(BankCard.new_bank_bard())
        url = 'https://xwbk.lanmaoly.com/bha-neo-app/gateway/mobile/personalRegisterExpand/register'
        payload = {'serviceType:': 'BANKCARD_AUTH', 'realName': '小明', 'credType': 'PRC_ID',
                   'idCardNo': str(IdentityCard().create_card()), 'bankcardNo': self.bank_card, 'mobile': self.mobile,
                   'smsCode': '111111', 'smsCount': '38', 'failTime': '2023年05月26日', 'defaultValue': 'false',
                   'authLimitSwitch': 'true', 'amount': '1000000', 'password': '111111', 'confirmPassword': '111111',
                   'protocolCheckBox': 'false', 'requestKey': self.key}
        print payload
        res = self.requests_template(url=url, data=payload)
        self.open_bank_account()

    def open_bank_account(self):
        """
        check用户是否开户
        """
        payload = self.open_bank_account_data
        payload['statics']['user_id'] = self.user_key
        payload['statics']['token'] = self.token
        payload['statics']['timestamp'] = self.unix_timestamp()
        print payload
        res = self.requests_template(url=self.config['config']['url'], data=json.dumps(payload))
        if res['openXWBankAccount']['error_code'] == 0:
            print res
            return True
        else:
            return False

    def recharge(self):
        """
        新网充值
        """
        self.register()
        url = 'https://xwbk.lanmaoly.com/bha-neo-app/lanmaotech/gateway'
        payload = self.config['USER_RECHARGE']['req_data']
        payload['timestamp'] = str(self.timestamp())
        payload['platformUserNo'] = str(self.u_id)
        payload['requestNo'] = str(self.generate_uuid())
        payload['expired'] = str(self.timestamp() + 600)
        payload['amount'] = self.money
        sign = self.generate_sign(str(payload))
        recharge_data = self.config['dlan_payload']
        recharge_data['serviceName'] = 'RECHARGE'
        recharge_data['reqData'] = str(payload)
        recharge_data['sign'] = str(sign)
        res = self.requests_template(url=url, data=recharge_data)
        print res
        soup = BeautifulSoup(res, "html.parser")
        a = soup.find_all('input')
        for link in a:
            b = link.get('value')
            if b:
                c = b.encode('unicode-escape').decode('string_escape')
                if c:
                    if '-' in c and '/' not in c:
                        tools.log().info(c)
                        self.key = c
                        return c

    def input_passwd(self):
        """
        输入交易密码
        """
        self.recharge()
        url = 'https://xwbk.lanmaoly.com/bha-neo-app/gateway/mobile/recharge/rechargeSwift.do'
        payload = {'maskedBankcardNo': self.bank_card_tail(), 'pageBank': 'EVER', 'projectName': '',
                   'maskedMobile': self.mobile_hide(), 'needSecurityCode': 'false', 'password': '111111',
                   'requestKey': self.key}
        print payload
        try:
            res = self.requests_template(url=url, data=payload)
            tools.log().info(res)
            return '创建成功'
        except:
            return '创建失败'



class IdentityCard(object):

    @staticmethod
    def get_address_no():
        """
        依据前17位数计算第18位的值并拼接成完整身份证号
        :return:
        """
        addressNo = ["110101", "110102", "110103", "110104", "110105", "110106", "110107", "110108", "110109", "110111",
                     "110112", "110113", "110221", "110224", "110226", "110227", "110228", "110229", ]
        return random.choice(addressNo)

    @staticmethod
    def get_birth():

        """
         随机生成生日
         """
        year = random.randint(1949, datetime.datetime.now().year - 18)
        month = random.randint(1, 12)
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        elif month in [4, 6, 9, 11]:
            day = random.randint(1, 30)
        else:
            if (year % 100 == 0 and year % 400 == 0) or (year % 100 != 0 and year % 4 == 0):
                day = random.randint(1, 29)
            else:
                day = random.randint(1, 28)
        if str(month).__len__() == 1:
            month = "0" + str(month)
        if str(day).__len__() == 1:
            day = "0" + str(day)
        return str(year) + str(month) + str(day)

    @staticmethod
    def get_sequence_no():
        """
          随机生成15-17位(100-500之间随机数)
          """
        return str(random.randint(100, 500))

    @staticmethod
    def get_check_no():
        """
           依据前17位数计算第18位的值并拼接成完整身份证号
           """
        data = IdentityCard.get_address_no() + IdentityCard.get_birth() + IdentityCard.get_sequence_no()
        coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        result = 0
        for char, coefficient in zip(data, coefficients):
            result += int(char) * coefficient
        checkNoList = {0: 1, 1: 0, 2: "X", 3: 9, 4: 8, 5: 7, 6: 6, 7: 5, 8: 4, 9: 3, 10: 2}
        data += str(checkNoList[result % 11])
        return data

    @staticmethod
    def create_card():

        return IdentityCard.get_check_no()


class BankCard(object):
    """
    生成招商银行卡
    """

    @staticmethod
    def bank_card():
        numberList = []
        for i in range(0, 1000):
            numberList.append(i)
        number = random.choice(numberList)
        return 6214830101460133 + number

    @staticmethod
    def new_bank_bard():
        numberList = []
        for i in range(0, 1000000):
            numberList.append(i)
        number = random.choice(numberList)
        return 6226620607792207 + number


if __name__ == '__main__':


    print 'haha'
    # mobile = 19012360000
    #  n = 0
    #  while int(n)<=100000:
    #    print '开始'
    #    try:
    #        phone = int(mobile) + int(n)
    #        create = XWCreate(phone)
    #        create.input_passwd()
    #    except:
    #        tools.log().error(phone)
    #    n+=1
