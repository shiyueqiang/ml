# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: create_user.py
@time: 2018/8/2 下午3:33
@desc:
"""
from app.service.user.nuser import XWCreate
from app.service.user.ouser import OldUser
from app.utils.common import tools
from app import dbo
from . import sqlData

class CreateUser:
    """
    创建三种类型用户
    """
    @staticmethod
    def user(data):
        phone = data['phone']
        if len(phone) ==11:
            result = dbo.db_query(tools.get_sql(sqlData, 'user', (str(phone),)))
            if not result:
                num = data['number']
                money = int(data['money'])
                print money
                plat = data['type']
                platform = data['platform']
                if plat == 'new':
                    try:
                        for item in range(0, int(num)):
                            mobile = int(phone) + item
                            user = XWCreate(mobile, money, platform)
                            user.input_passwd()
                        return "创建成功"
                    except Exception as e:
                        print e
                        return '创建失败'

                elif plat == 'old':
                    try :
                        for item in range(0, int(num)):
                            mobile = int(phone) + item
                            oldUser = OldUser(mobile)
                            oldUser.register()
                            oldUser.set_login_password()
                            oldUser.bind_card()
                            oldUser.bind_card_verify()
                            oldUser.update_default()
                            oldUser.update_user_role()
                            oldUser.add_zx_sub()
                        return "创建成功"
                    except Exception as e:
                        print e
                        return '创建失败'
                else:
                    return '您输入的平台不存在'
            else:
                return '手机号已存在'
        else:
            return '手机号非法'


create = CreateUser()