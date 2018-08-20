# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: ouser.py
@time: 2018/8/1 下午4:55
@desc:
"""
import json
from app import dbo, dbn, config
from . import ouserPath, ouser_sql
from app.utils.requester import requester
from app.utils.common import tools

class OldUser:

    def __init__(self, phone):
        """
        数据初始化
        """
        self.phone = phone
        self.s = requester
        self.api = config['app'] + 'v12'
        self.old_api = config['old_app']+'v11'
        self.login = False
        self.token = None
        self.user_key = None
        self.u_id = None

    def register(self):
        """
        用户注册
        """
        try:
            payload =tools.get_json(tools.get_path(ouserPath, 'old_register'))
            payload['fun']['register']['mobile'] = self.phone
            res = self.s.post(url=self.api, data=json.dumps(payload))
            if res.json()['register']['error_code'] == 0:
                self.token = res.json()['register']['data']['token']
                self.user_key = res.json()['register']['data']['userKey']
                self.u_id = res.json()['register']['data']['user_id']
                print res.json()
            else:
                print res.text
        except Exception as e:
            tools.log().error(e)

    def set_login_password(self):
        """
        设置登录密码
        """
        payload = tools.get_json(tools.get_path(ouserPath, 'set_password'))
        # payload = read_json('set_password')
        payload['statics']['token'] = self.token
        payload['statics']['user_id'] = self.u_id

        print(payload)
        res = self.s.post(url=self.api, data=json.dumps(payload))
        print res.json()

    def bind_card(self):
        """
        绑卡
        """
        payload = tools.get_json(tools.get_path(ouserPath, 'bind_card'))
        # payload = read_json('bind_card')
        payload['fun']['bind_card_v2_1']['bank_mobile'] = self.phone
        payload['fun']['bind_card_v2_1']['id_card'] = IdentityCard.create_card()
        payload['fun']['bind_card_v2_1']['bank_card'] = BankCard.bank_card()
        payload['statics']['token'] = self.token
        payload['statics']['user_id'] = self.u_id
        print(payload)
        res = self.s.post(url=self.old_api, data=json.dumps(payload))
        print res.json()

    def bind_card_verify(self):
        """
        验卡
        """
        payload = tools.get_json(tools.get_path(ouserPath, 'bind_card_verify'))
        # payload = read_json('bind_card_verify')
        payload['statics']['token'] = self.token
        payload['statics']['user_id'] = self.u_id
        res = self.s.post(url=self.old_api, data=json.dumps(payload))
        print res.json()
        return res.json()['bind_card_verify']['data']['id_card'], res.json()['bind_card_verify']['data']['bank_card']


    def update_default(self):
        """
        更新数据库数据
        """

        dbo.db_insert(get_sql('update_old_user_java'))
        dbo.db_insert(get_sql('update_old_user_php'))
        print '更新数据库完毕'

    def update_user_role(self):
        """
        更改用户所属平台
        """
        dbo.db_insert(tools.get_sql(ouser_sql, 'set_role_old', (self.phone,)))

    def add_zx_sub(self):
        """
        添加用户尊享账户
        """
        dbo.db_insert(tools.get_sql(ouser_sql, 'add_old_user_zx_sub', (tools.generate_uuid(), self.u_id,)))
