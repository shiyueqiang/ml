# coding:utf-8
"""
@version: 
@author: shiyueqiang 
@file: __init__.py.py
@time: 2018/7/30 上午10:35
@desc:
"""
from flask import Flask
from app.utils.db import DB
from app.utils.common import tools
from app.config.pathconfig import *

# 获取sql数据配置
config = tools.get_config(envConfigPath)
sqlYml = os.path.join(sqlPath, 'sql.yml')
sqlPool = tools.get_yml(sqlYml)

if config['env']['model']:
    dbn = DB(host=config['dbn']['host'], port=config['dbn']['port'], user=config['dbn']['user'], passwd=config['dbn']['passwd'])
    dbo = DB(host=config['dbo']['host'], port=config['dbo']['port'], user=config['dbo']['user'], passwd=config['dbo']['passwd'])
else:
    dbn = DB(host='127.0.0.1', port=3307, user=config['dbn']['user'], passwd=config['dbn']['passwd'])
    dbo = DB(host='127.0.0.1', port=3306, user=config['dbo']['user'], passwd=config['dbo']['passwd'])

mydb = DB(host='192.168.100.215', port=3306, user=config['dbo']['user'], passwd=config['dbo']['passwd'])

def create_app(config_filename):
    """
    启动flask应用
    """
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)


    app.config['SECRET_KEY'] = 'Xc0utYanW6JBYqUGr7VENFxMtq7PnJob'


    from .main import main as main
    from .main import user as user
    from .main import service as service
    from .main import test as test

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(service, url_prefix='/service')
    app.register_blueprint(test, url_prefix='/test')


    return app


